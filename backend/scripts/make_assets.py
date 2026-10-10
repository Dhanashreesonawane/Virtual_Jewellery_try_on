"""Generate original placeholder PNG jewellery + catalog (no copyrighted art).
Replace the PNGs with your own transparent assets, keeping the same paths."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "app" / "data"
S = 4  # supersample
GOLDS = {"gold": (212, 175, 55), "rose": (214, 150, 130)}


def canvas(w, h):
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(im, rel, size):
    p = ROOT / "assets" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.resize(size, Image.LANCZOS).save(p)


def ring(rel, col, gem):
    im, d = canvas(200, 70)
    d.rounded_rectangle((8 * S, 14 * S, 192 * S, 56 * S), 20 * S, fill=col + (255,))
    d.rounded_rectangle((8 * S, 20 * S, 192 * S, 30 * S), 5 * S, fill=(255, 245, 200, 140))
    if gem:
        d.ellipse((80 * S, 2 * S, 120 * S, 42 * S), fill=(120, 190, 230, 255), outline=col + (255,), width=4 * S)
    save(im, rel, (200, 70))


def bangle(rel, col):
    im, d = canvas(300, 90)
    d.rounded_rectangle((4 * S, 10 * S, 296 * S, 80 * S), 35 * S, outline=col + (255,), width=14 * S)
    save(im, rel, (300, 90))


def earring(rel, col):
    im, d = canvas(60, 160)
    d.ellipse((22 * S, 2 * S, 38 * S, 18 * S), fill=col + (255,))
    d.line((30 * S, 16 * S, 30 * S, 60 * S), fill=col + (255,), width=3 * S)
    d.polygon([(30 * S, 60 * S), (52 * S, 105 * S), (30 * S, 156 * S), (8 * S, 105 * S)], fill=col + (255,))
    d.polygon([(30 * S, 75 * S), (42 * S, 105 * S), (30 * S, 135 * S), (18 * S, 105 * S)], fill=(255, 245, 200, 180))
    save(im, rel, (60, 160))


def necklace(rel, col, pendant):
    im, d = canvas(400, 300)
    d.arc((10 * S, -150 * S, 390 * S, 250 * S), 0, 180, fill=col + (255,), width=6 * S)
    if pendant:
        d.polygon([(200 * S, 235 * S), (225 * S, 262 * S), (200 * S, 292 * S), (175 * S, 262 * S)], fill=(150, 30, 60, 255), outline=col + (255,), width=4 * S)
    save(im, rel, (400, 300))


items = []
def add(cat, n, name, anchor, scale=1.0):
    i = f"{cat}_{n:03d}"
    rel = f"assets/{cat}s/{i}.png"
    items.append(dict(id=i, name=name, category=cat, asset_path=rel, thumbnail_path=rel,
                      anchor_type=anchor, default_scale=scale, rotation_offset=0,
                      x_offset=0, y_offset=0, enabled=True))
    return rel[len("assets/"):]

ring(add("ring", 1, "Classic Gold Band", "ring_finger"), GOLDS["gold"], False)
ring(add("ring", 2, "Sapphire Solitaire", "ring_finger"), GOLDS["rose"], True)
bangle(add("bangle", 1, "Gold Bangle", "wrist"), GOLDS["gold"])
bangle(add("bangle", 2, "Rose Gold Bangle", "wrist"), GOLDS["rose"])
earring(add("earring", 1, "Gold Drop Earrings", "ear_lobe"), GOLDS["gold"])
earring(add("earring", 2, "Rose Gold Drops", "ear_lobe"), GOLDS["rose"])
necklace(add("necklace", 1, "Fine Gold Chain", "neck"), GOLDS["gold"], False)
necklace(add("necklace", 2, "Ruby Pendant", "neck"), GOLDS["gold"], True)
(ROOT / "jewelry_catalog.json").write_text(json.dumps(items, indent=2))
print(f"wrote {len(items)} items")
