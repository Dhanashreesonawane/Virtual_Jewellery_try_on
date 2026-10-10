"""Try-on pipeline: preprocess -> detect -> track -> smooth -> align -> render."""
import logging
import uuid
from functools import lru_cache
from time import perf_counter
import cv2
import numpy as np
from ..core.config import settings
from ..core.errors import AppError
from ..detectors import mediapipe_detectors as det
from ..models.schemas import JewelryItem
from ..trackers.trackers import BangleTracker, EarringTracker, NecklaceTracker, RingTracker, describe
from ..utils.image_utils import denoise, normalize, to_rgb
from ..utils.validation import validate_category
from . import alignment_service as A
from .enhancer import BasicEnhancer
from .occlusion_service import hand_clip_mask
from .overlay_service import composite_jewelry, render_jewelry

log = logging.getLogger("tryon")
ENHANCER = BasicEnhancer()


@lru_cache(maxsize=64)
def load_asset(path: str) -> np.ndarray:
    full = (settings.data_dir / path).resolve()
    if settings.data_dir.resolve() not in full.parents:
        raise AppError("JEWELRY_NOT_FOUND", "Invalid asset path.", 404)
    img = cv2.imread(str(full), cv2.IMREAD_UNCHANGED)
    if img is None or img.ndim != 3 or img.shape[2] != 4:
        raise AppError("PROCESSING_FAILED", "Jewellery asset must be a transparent PNG.", 500)
    return img


def find_placements(rgb, item: JewelryItem, side: str, live: bool):
    cat = item.category
    if cat in ("ring", "bangle"):
        hands = det.detect_hands(rgb, live)
        if not hands:
            raise AppError("NO_HAND_DETECTED", "No suitable hand was detected.")
        hand = max(hands, key=lambda h: h.score)
        tracker = RingTracker(item.anchor_type or "ring_finger") if cat == "ring" else BangleTracker()
        pls = tracker.track(hand)
        for p in pls:
            p.clip_pts = hand.pts if cat == "ring" else None   # occlusion: keep rings on the hand
        return pls, {"hands": len(hands)}
    if cat == "earring":
        face = det.detect_face(rgb, live)
        if face is None:
            raise AppError("NO_FACE_DETECTED", "No face was detected.")
        return EarringTracker(side).track(face), {"faces": 1}
    pose = det.detect_pose(rgb, live)
    if pose is None:
        raise AppError("NO_POSE_DETECTED", "No upper body was detected.")
    face = det.detect_face(rgb, live)
    return NecklaceTracker().track(pose, face), {"poses": 1, "faces": int(face is not None)}


def process_frame(image: np.ndarray, item: JewelryItem, category: str, side: str = "both",
                  clean: bool = False, max_side: int | None = None, live: bool = False,
                  smoother=None) -> tuple[np.ndarray, dict]:
    """Returns (processed BGR image, metadata). Raises AppError when tracking fails."""
    validate_category(category)
    if item.category != category:
        raise AppError("INVALID_CATEGORY", "Selected jewellery does not match the category.")
    timings = {}
    t = perf_counter()
    img = normalize(image, max_side)
    if clean:
        img = denoise(img)
    rgb = to_rgb(img)
    asset = load_asset(item.asset_path)
    timings["preprocess_ms"] = (perf_counter() - t) * 1000

    t = perf_counter()
    placements, summary = find_placements(rgb, item, side, live)
    timings["landmarks_ms"] = (perf_counter() - t) * 1000

    t = perf_counter()
    if smoother:
        placements = smoother(placements)
    plans = []
    for pl in placements:   # recomputed from this frame's landmarks, every frame
        scale = A.calculate_scale(pl.width, asset.shape[1], item.default_scale)
        rot = A.calculate_rotation(pl.rotation, item.rotation_offset)
        c = A.calculate_translation(pl.center, asset.shape[0] * scale, pl.anchor_y, rot,
                                    item.x_offset, item.y_offset, asset.shape[1] * scale)
        plans.append((pl, scale, rot, c))
    timings["alignment_ms"] = (perf_counter() - t) * 1000

    t = perf_counter()
    out = img.copy()
    for pl, scale, rot, (cx, cy) in plans:
        piece = render_jewelry(asset, scale, rot)
        mask = hand_clip_mask(out.shape, pl.clip_pts, pl.width * 0.35) if pl.clip_pts is not None else None
        composite_jewelry(out, piece, mask, (round(cx - piece.shape[1] / 2), round(cy - piece.shape[0] / 2)))
    out = ENHANCER.enhance(out, asset, None)
    timings["render_ms"] = (perf_counter() - t) * 1000

    total = sum(timings.values())
    meta = {
        "processing_time_ms": round(total, 1),
        "fps_estimate": round(1000 / total, 1) if total else None,
        "category": category, "jewelry_id": item.id,
        "timings_ms": {k: round(v, 1) for k, v in timings.items()},
        "confidence": round(float(np.mean([p.confidence for p in placements])), 3),
        "landmarks_summary": summary,
        "trackers": [describe(p) for p in placements],
        "transform": [{"center": [round(c[0], 1), round(c[1], 1)], "scale": round(s, 3),
                       "rotation_deg": round(r, 1)} for _, s, r, c in plans],
    }
    return out, meta


def run_tryon(image, item, category, side="both", clean=False, max_side=None) -> dict:
    out, meta = process_frame(image, item, category, side, clean, max_side)
    name = f"{uuid.uuid4().hex}.jpg"
    cv2.imwrite(str(settings.outputs_dir / name), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
    log.info("tryon category=%s total_ms=%.1f", category, meta["processing_time_ms"])
    return {"image_url": f"/outputs/{name}", **meta}
