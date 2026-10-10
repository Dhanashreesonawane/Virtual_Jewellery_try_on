"""Measured pipeline speed on one image, in live mode (640px, tracking + smoothing).
  python scripts/benchmark.py photo.jpg ring_001 ring -n 50"""
import argparse
import statistics as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.database.repositories import jewelry_repo
from app.services.smoothing import PlacementSmoother
from app.services.tryon_service import process_frame
from app.utils.image_utils import decode_image

ap = argparse.ArgumentParser()
ap.add_argument("image"); ap.add_argument("jewelry_id"); ap.add_argument("category")
ap.add_argument("-n", type=int, default=50); ap.add_argument("--side", default="both")
a = ap.parse_args()
img = decode_image(Path(a.image).read_bytes())
item, sm = jewelry_repo().get(a.jewelry_id), PlacementSmoother()
run = lambda: process_frame(img, item, a.category, a.side, max_side=640, live=True, smoother=sm)[1]
run()  # warm-up (model load) is not counted
runs = [run() for _ in range(a.n)]
tot = [r["processing_time_ms"] for r in runs]
fps = [1000 / t for t in tot]
col = lambda k: [r["timings_ms"][k] for r in runs]
print(f"frames {a.n}")
print(f"avg processing  {st.mean(tot):.1f} ms")
print(f"landmarks avg   {st.mean(col('landmarks_ms')):.1f} ms")
print(f"rendering avg   {st.mean(col('render_ms')):.1f} ms")
print(f"FPS avg/min/max {st.mean(fps):.1f} / {min(fps):.1f} / {max(fps):.1f}  (processing only, excludes network)")
