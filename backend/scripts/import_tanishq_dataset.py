"""Import a LOCAL jewellery dataset (supplied by you) into assets + MongoDB.

  tanishq_dataset/{rings,bangles,earrings,necklaces}/*.jpg|png|webp
  python scripts/import_tanishq_dataset.py tanishq_dataset [--metadata meta.csv] [--no-db]

Optional metadata (CSV or JSON list) columns: file, name, price, description, brand.
Without --no-db, documents go to MongoDB (needs MONGO_URI); with it, to app/data/jewelry_catalog.json.
3D model files (.glb/.obj/...) are skipped: this 2D pipeline needs images. Render a front view first.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.services.asset_service import make_thumbnail, prepare_asset

ROOT = Path(__file__).resolve().parents[1] / "app" / "data"
FOLDERS = {"rings": "ring", "bangles": "bangle", "earrings": "earring", "necklaces": "necklace"}
TRACK = {"ring": ("hand", "ring_finger"), "bangle": ("hand", "wrist"),
         "earring": ("face", "ear_lobe"), "necklace": ("pose", "neck")}
IMG, MODEL = {".jpg", ".jpeg", ".png", ".webp"}, {".glb", ".gltf", ".obj", ".fbx", ".stl", ".usdz"}


def load_metadata(path):
    if not path:
        return {}
    p = Path(path)
    rows = json.loads(p.read_text()) if p.suffix == ".json" else list(csv.DictReader(p.open(encoding="utf-8")))
    return {Path(r["file"]).name: r for r in rows if r.get("file")}


def build_docs(dataset: Path, meta: dict, brand: str):
    skipped = {"3d_models": 0, "invalid": 0}
    for folder, cat in FOLDERS.items():
        d = dataset / folder
        if not d.is_dir():
            print(f"  (no '{folder}' folder, skipping)")
            continue
        for n, f in enumerate(sorted(p for p in d.rglob("*") if p.is_file()), 1):
            ext = f.suffix.lower()
            if ext in MODEL:
                skipped["3d_models"] += 1
                continue
            img = cv2.imread(str(f), cv2.IMREAD_UNCHANGED) if ext in IMG else None
            if img is None or min(img.shape[:2]) < 32:
                skipped["invalid"] += 1
                print(f"  invalid image: {f.name}")
                continue
            try:
                asset = prepare_asset(img)
            except ValueError as e:
                skipped["invalid"] += 1
                print(f"  {f.name}: {e}")
                continue
            pid = f"{cat}_{n:04d}"                      # our own id; never derived from file names
            for sub in ("original", "transparent", "thumbnails"):
                (ROOT / "assets" / sub).mkdir(parents=True, exist_ok=True)
            orig = ROOT / "assets" / "original" / f"{pid}{ext}"
            orig.write_bytes(f.read_bytes())
            cv2.imwrite(str(ROOT / "assets" / "transparent" / f"{pid}.png"), asset)
            cv2.imwrite(str(ROOT / "assets" / "thumbnails" / f"{pid}.png"), make_thumbnail(asset))
            m = meta.get(f.name, {})
            lm, anchor = TRACK[cat]
            price = m.get("price")
            yield {
                "_id": pid, "name": m.get("name") or re.sub(r"[_\-]+", " ", f.stem).strip().title(),
                "brand": m.get("brand") or brand, "category": cat, "description": m.get("description") or "",
                "price": float(price) if price not in (None, "") else None,
                "original_image": f"assets/original/{pid}{ext}",
                "transparent_asset": f"assets/transparent/{pid}.png",
                "thumbnail": f"assets/thumbnails/{pid}.png",
                "landmark_type": lm, "anchor": anchor, "default_scale": 1.0,
                "rotation_offset": 0, "x_offset": 0, "y_offset": 0, "active": True}
    print("skipped:", skipped)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset"); ap.add_argument("--metadata"); ap.add_argument("--brand", default="Tanishq")
    ap.add_argument("--no-db", action="store_true")
    a = ap.parse_args()
    docs = list(build_docs(Path(a.dataset), load_metadata(a.metadata), a.brand))
    if a.no_db:
        (ROOT / "jewelry_catalog.json").write_text(json.dumps(docs, indent=2))
        print(f"wrote {len(docs)} items to jewelry_catalog.json")
        return
    from app.database.mongodb import get_db
    db = get_db()
    if db is None:
        sys.exit("MONGO_URI is not set. Set it, or use --no-db.")
    for d in docs:
        db["jewellery"].replace_one({"_id": d["_id"]}, d, upsert=True)
    print(f"upserted {len(docs)} items into MongoDB")


if __name__ == "__main__":
    main()
