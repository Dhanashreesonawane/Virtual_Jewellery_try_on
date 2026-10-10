import numpy as np
import pytest
from app.core.errors import AppError
from app.models.jewelry import Detection
from app.processors import placements as P


def fake_hand():
    p = np.zeros((21, 2), np.float32)
    p[0] = (100, 300); p[9] = (100, 200)             # wrist, middle knuckle (finger up)
    p[5] = (60, 200); p[17] = (140, 200)             # palm width 80
    p[13], p[14] = (120, 200), (120, 160)            # ring finger knuckle/pip
    return Detection(p, 0.9)


def test_ring_follows_finger():
    pl = P.ring_placement(fake_hand(), "ring_finger")
    assert pl.center == (120, 180) and pl.rotation == 0 and pl.width == pytest.approx(21)


def test_bangle_below_wrist():
    pl = P.bangle_placement(fake_hand())
    assert pl.center[1] > 300 and pl.width == pytest.approx(88)


def test_necklace_low_visibility_rejected():
    pts = np.zeros((33, 2), np.float32)
    with pytest.raises(AppError):
        P.necklace_placement(Detection(pts, 0.1, np.zeros(33, np.float32)))
