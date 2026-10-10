"""JSON-file storage behind repository classes (swap for a DB later)."""
import json
import threading
import time
import uuid
from pathlib import Path
from ..core.config import settings
from ..core.errors import AppError
from ..models.schemas import JewelryItem


def to_item(d: dict) -> JewelryItem:
    """Accept both DB documents (_id, transparent_asset, anchor, active) and old catalog entries."""
    asset = d.get("transparent_asset", d.get("asset_path"))
    return JewelryItem(
        id=str(d.get("_id", d.get("id"))), name=d["name"], category=d["category"], asset_path=asset,
        thumbnail_path=d.get("thumbnail", d.get("thumbnail_path", asset)),
        anchor_type=d.get("anchor", d.get("anchor_type", "")),
        default_scale=d.get("default_scale", 1.0), rotation_offset=d.get("rotation_offset", 0.0),
        x_offset=d.get("x_offset", 0.0), y_offset=d.get("y_offset", 0.0),
        enabled=d.get("active", d.get("enabled", True)),
        brand=d.get("brand"), description=d.get("description"), price=d.get("price"))


class JewelryRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or settings.data_dir / "jewelry_catalog.json"

    def all(self, category: str | None = None) -> list[JewelryItem]:
        items = [to_item(d) for d in json.loads(self.path.read_text())]
        return [i for i in items if i.enabled and (category is None or i.category == category)]

    def get(self, jewelry_id: str) -> JewelryItem:
        for i in self.all():
            if i.id == jewelry_id:
                return i
        raise AppError("JEWELRY_NOT_FOUND", "That jewellery item does not exist.", 404)


class ResultRepository:
    def __init__(self, path: Path | None = None):
        self.path = path or settings.outputs_dir / "results.json"
        self._lock = threading.Lock()

    def all(self) -> list[dict]:
        return json.loads(self.path.read_text()) if self.path.exists() else []

    def add(self, record: dict) -> dict:
        record = {"id": uuid.uuid4().hex[:12], "saved_at": time.time(), **record}
        with self._lock:
            rows = self.all()
            rows.insert(0, record)
            self.path.write_text(json.dumps(rows, indent=2))
        return record
