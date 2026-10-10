import numpy as np
from app.models.jewelry import Placement
from app.services.smoothing import PlacementSmoother
from app.trackers.trackers import RingTracker, describe
from tests.test_landmarks import fake_hand


def test_ring_moves_scales_rotates_with_finger():
    a = RingTracker().track(fake_hand())[0]
    h = fake_hand(); h.pts = h.pts * 2 + 50          # hand moves and gets closer
    b = RingTracker().track(h)[0]
    assert b.center != a.center and b.width > a.width
    h2 = fake_hand(); h2.pts[14] = (160, 200)         # finger now points sideways
    assert RingTracker().track(h2)[0].rotation != a.rotation


def test_smoother_blends_and_takes_short_way_round():
    s = PlacementSmoother(alpha=0.5)
    s([Placement((0, 0), 10, 170, 0.5, 1)])
    out = s([Placement((10, 0), 20, -170, 0.5, 1)])[0]
    assert out.center == (5, 0) and out.width == 15 and abs(abs(out.rotation) - 180) < 1e-6


def test_describe_keys():
    assert set(describe(Placement((1, 2), 3, 4, 0, 1))) == {"center", "scale", "rotation", "confidence"}
