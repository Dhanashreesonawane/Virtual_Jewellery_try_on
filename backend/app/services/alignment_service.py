"""Reusable transform maths: scale, rotation, translation, affine, perspective."""
import cv2
import numpy as np


def calculate_scale(target_width: float, asset_width: int, default_scale: float = 1.0) -> float:
    return max(target_width * default_scale / max(asset_width, 1), 1e-3)


def calculate_rotation(placement_rotation: float, offset: float = 0.0) -> float:
    return placement_rotation + offset


def calculate_translation(anchor, asset_h: float, anchor_y: float, rotation: float,
                          x_off: float = 0.0, y_off: float = 0.0, asset_w: float = 0.0):
    """Centre of the (scaled, unrotated) asset so its anchor point lands on `anchor`.
    The offset from anchor to centre is rotated together with the asset."""
    t = np.deg2rad(rotation)
    vx, vy = x_off * asset_w, (0.5 - anchor_y) * asset_h + y_off * asset_w
    return (anchor[0] + vx * np.cos(t) + vy * np.sin(t),
            anchor[1] - vx * np.sin(t) + vy * np.cos(t))


def create_affine_matrix(center, angle: float, scale: float = 1.0) -> np.ndarray:
    return cv2.getRotationMatrix2D(center, angle, scale)


def apply_perspective_transform(img: np.ndarray, src_quad, dst_quad, size) -> np.ndarray:
    """Homography warp (used when a jewelry piece must be bent, e.g. a necklace)."""
    H = cv2.getPerspectiveTransform(np.float32(src_quad), np.float32(dst_quad))
    return cv2.warpPerspective(img, H, size, flags=cv2.INTER_LINEAR,
                               borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
