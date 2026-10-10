import numpy as np
from app.services import alignment_service as A
from app.utils.geometry import angle_deg, upright_rotation


def test_scale():
    assert A.calculate_scale(100, 200, 1.0) == 0.5


def test_upright_rotation_for_finger_pointing_up_is_zero():
    assert upright_rotation(angle_deg((0, 10), (0, 0))) == 0


def test_translation_top_anchor_moves_centre_down():
    cx, cy = A.calculate_translation((100, 100), 80, 0.0, 0.0)
    assert (cx, cy) == (100, 140)


def test_affine_identity():
    assert np.allclose(A.create_affine_matrix((5, 5), 0)[:, :2], np.eye(2))
