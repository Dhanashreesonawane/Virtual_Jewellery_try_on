import numpy as np
from app.services.overlay_service import composite_jewelry, render_jewelry


def test_opaque_pixel_replaces_background():
    bg = np.zeros((20, 20, 3), np.uint8)
    jw = np.zeros((4, 4, 4), np.uint8); jw[..., 2] = 255; jw[..., 3] = 255
    out = composite_jewelry(bg, render_jewelry(jw, 1.0, 0), None, (5, 5))
    assert out[6, 6].tolist() == [0, 0, 255] and out[0, 0].tolist() == [0, 0, 0]


def test_transparent_leaves_background():
    bg = np.full((10, 10, 3), 50, np.uint8)
    jw = np.zeros((4, 4, 4), np.uint8)
    assert (composite_jewelry(bg, render_jewelry(jw, 1, 0), None, (2, 2)) == 50).all()


def test_offscreen_does_not_crash():
    bg = np.zeros((10, 10, 3), np.uint8)
    composite_jewelry(bg, np.ones((6, 6, 4), np.float32), None, (-20, 30))


def test_rotation_grows_canvas():
    assert render_jewelry(np.ones((10, 40, 4), np.uint8), 1.0, 90).shape[:2] == (40, 10)
