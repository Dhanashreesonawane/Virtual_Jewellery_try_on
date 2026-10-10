# Virtual Jewellery Try-On: Backend

FastAPI + MediaPipe + OpenCV. Upload a photo or send webcam frames; get back the image with jewellery placed on hand, wrist, ears or neck.

## Pipeline
decode/validate -> resize -> MediaPipe landmarks -> placement (centre, width, rotation) -> scale/rotate/translate -> alpha composite -> optional enhancer -> JPEG in `outputs/`

| Category | Detector | Landmarks used |
|---|---|---|
| ring | Hands | finger knuckle (MCP) and middle joint (PIP); finger width = palm width / 4 |
| bangle | Hands | wrist (0), middle knuckle (9) for direction, palm width for size |
| earring | Face Mesh | cheek edges 234/454, forehead 10, chin 152; anchor sits below the edge (approximate ear lobe) |
| necklace | Pose | shoulders 11/12, mouth 9/10; width = half the shoulder span |

## Setup
    python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env
    python scripts/make_assets.py        # creates original placeholder PNGs + catalog
    uvicorn app.main:app --reload --env-file .env
Check: `curl localhost:8000/api/health`. Docs: http://localhost:8000/docs

## API (all JSON: `{success, data, error}`)
- GET `/api/health`, GET `/api/jewelry?category=ring`, GET `/api/jewelry/{id}`
- POST `/api/tryon/image` (multipart: image, jewelry_id, category, side=both|left|right)
- POST `/api/tryon/frame` (JSON: image base64/data URL, jewelry_id, category)
- POST `/api/results` (JSON: image_url from a try-on, jewelry_id, category), GET `/api/results`

    curl -F image=@hand.jpg -F jewelry_id=ring_001 -F category=ring localhost:8000/api/tryon/image

## Your own jewellery
Add a transparent RGBA PNG under `app/data/assets/<type>s/` and an entry in `jewelry_catalog.json`. Draw it upright: rings/bangles face-on with the band across the width; earrings and necklaces with the attachment point at the top centre.

## Tests and benchmark
    pytest
    python scripts/benchmark.py photo.jpg ring_001 ring -n 20   # real measured timings

## Known limitations
- 2D overlay only. Occlusion is heuristic: rings are clipped to the hand outline; no hair, neck or depth handling.
- Earring and necklace positions are estimated from face-edge and shoulder landmarks, not true ear or neck contours.
- Left/right earring means image-left/right. Live mode processes one frame per request.
- `BasicEnhancer` does nothing. `JewelryEnhancer` in `services/enhancer.py` is the hook for a future GAN.
- Detectors for hand, face and pose live in one module, and ROI logic in `processors/placements.py`, rather than one file per type.

## Live camera (WebSocket `/ws/tryon`)
Client sends a JSON config `{jewelry_id, category, side}` then binary JPEG frames (unmirrored). For each frame the server replies with a JSON metadata message (`tracking`, `landmark_detected`, `processing_time_ms`, `fps_estimate`, `stream_fps`, `trackers`, ...) and then the processed JPEG (the original frame when tracking is lost). The client sends the next frame only after the reply. Every frame re-detects landmarks and recomputes position, scale and rotation; `PlacementSmoother` only reduces jitter. `fps_estimate` is processing speed; `stream_fps` is the measured delivered rate.

## MongoDB and dataset import
Set `MONGO_URI` to store the catalog and results in MongoDB (`jewellery`, `tryon_results`); without it, JSON files are used. Import your own dataset folder (`rings/ bangles/ earrings/ necklaces/` of product images, optional metadata CSV/JSON):

    python scripts/import_tanishq_dataset.py path/to/dataset --metadata meta.csv
    python scripts/import_tanishq_dataset.py path/to/dataset --no-db      # JSON catalog, no MongoDB

Background removal is colour-based and suits plain backgrounds. 3D model files are skipped; render a front view to an image first. Product photos are not automatically ideal overlays: rings and bangles need a flat, face-on band view, earrings and necklaces an upright view (a pair photo must be cropped to one earring). Tune `rotation_offset`, `x_offset`, `y_offset`, `default_scale` per item.
