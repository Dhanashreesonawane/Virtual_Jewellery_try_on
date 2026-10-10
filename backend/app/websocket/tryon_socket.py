"""WebSocket /ws/tryon  (stop-and-wait: the client sends the next frame after each reply)

Client -> server:
  text   {"jewelry_id": "...", "category": "ring", "side": "both"}   (sent on connect and on change)
  binary one JPEG/WebP/PNG frame (camera orientation, NOT mirrored)
Server -> client, per frame:
  text   {"tracking", "landmark_detected", "category", "processing_time_ms", "fps_estimate", "stream_fps", ...}
  binary processed JPEG (the original frame when tracking is lost)
"""
import json
import logging
from time import perf_counter
import cv2
from fastapi import APIRouter, WebSocket
from starlette.concurrency import run_in_threadpool
from ..core.config import settings
from ..core.errors import AppError
from ..database.repositories import jewelry_repo
from ..services.smoothing import PlacementSmoother
from ..services.tryon_service import process_frame
from ..utils.image_utils import decode_image
from ..utils.validation import validate_category

router = APIRouter()
repo = jewelry_repo()
log = logging.getLogger("ws")
LIVE_MAX_SIDE, JPEG_Q = 640, 80


def _live(frame: bytes, item, cfg, smoother):
    t0 = perf_counter()
    img = decode_image(frame)
    out, meta = process_frame(img, item, cfg["category"], cfg["side"], max_side=LIVE_MAX_SIDE,
                              live=True, smoother=smoother)
    ok, buf = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, JPEG_Q])
    total = (perf_counter() - t0) * 1000       # decode + track + render + encode
    meta.update(processing_time_ms=round(total, 1), fps_estimate=round(1000 / total, 1))
    return meta, buf.tobytes()


@router.websocket("/ws/tryon")
async def tryon_ws(ws: WebSocket):
    origin = ws.headers.get("origin")
    if origin and origin not in settings.origins:
        await ws.close(code=1008)
        return
    await ws.accept()
    cfg, item, smoother, last = None, None, PlacementSmoother(), None
    stream_fps = None
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            if msg.get("text") is not None:
                try:
                    d = json.loads(msg["text"])
                    cat = validate_category(d.get("category", ""))
                    item = repo.get(d.get("jewelry_id", ""))
                    cfg = {"category": cat, "side": d.get("side", "both")}
                    smoother.reset()
                except AppError as e:
                    cfg = None
                    await ws.send_json({"type": "error", "error": {"code": e.code, "message": e.message}})
                except ValueError:
                    await ws.send_json({"type": "error", "error": {"code": "INVALID_REQUEST", "message": "Bad config."}})
                continue
            frame = msg.get("bytes")
            if not frame or cfg is None:
                await ws.send_json({"type": "error", "error": {"code": "INVALID_REQUEST", "message": "Select jewellery first."}})
                continue
            now = perf_counter()
            if last:
                inst = 1 / max(now - last, 1e-6)
                stream_fps = inst if stream_fps is None else 0.8 * stream_fps + 0.2 * inst
            last = now
            try:
                meta, jpeg = await run_in_threadpool(_live, frame, item, cfg, smoother)
                meta.update(tracking=True, landmark_detected=True)
            except AppError as e:
                smoother.reset()
                meta, jpeg = {"tracking": False, "landmark_detected": False, "category": cfg["category"],
                              "error": {"code": e.code, "message": e.message}}, frame
            except Exception:
                log.exception("live frame failed")
                meta, jpeg = {"tracking": False, "landmark_detected": False, "category": cfg["category"],
                              "error": {"code": "PROCESSING_FAILED", "message": "Frame failed."}}, frame
            meta["stream_fps"] = round(stream_fps, 1) if stream_fps else None
            await ws.send_json(meta)
            await ws.send_bytes(jpeg)
    except Exception:
        log.info("socket closed")
