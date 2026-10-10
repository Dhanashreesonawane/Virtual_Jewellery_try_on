from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)


def test_list_and_filter():
    assert len(c.get("/api/jewelry").json()["data"]) == 8
    assert all(i["category"] == "ring" for i in c.get("/api/jewelry?category=ring").json()["data"])


def test_unknown_jewelry():
    r = c.get("/api/jewelry/nope")
    assert r.status_code == 404 and r.json()["error"]["code"] == "JEWELRY_NOT_FOUND"


def test_tryon_rejects_non_image():
    r = c.post("/api/tryon/image", files={"image": ("a.png", b"not an image", "image/png")},
               data={"jewelry_id": "ring_001", "category": "ring"})
    assert r.json()["error"]["code"] == "UNSUPPORTED_FORMAT"


def test_tryon_empty_and_bad_category():
    r = c.post("/api/tryon/image", files={"image": ("a.png", b"", "image/png")},
               data={"jewelry_id": "ring_001", "category": "hat"})
    assert r.json()["error"]["code"] == "INVALID_CATEGORY"


def test_save_rejects_path_traversal():
    r = c.post("/api/results", json={"image_url": "/outputs/../secret.jpg", "jewelry_id": "x", "category": "ring"})
    assert r.json()["error"]["code"] == "INVALID_RESULT"
