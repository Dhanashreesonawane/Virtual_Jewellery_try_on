import math
import numpy as np


def dist(a, b) -> float:
    return float(np.linalg.norm(np.asarray(a, float) - np.asarray(b, float)))


def angle_deg(a, b) -> float:
    """Direction a->b in image coordinates (y down), degrees."""
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def upright_rotation(direction_deg: float) -> float:
    """cv2 rotation so an asset drawn 'pointing up' follows a direction."""
    return -(direction_deg + 90.0)


def lerp(a, b, t: float) -> np.ndarray:
    a, b = np.asarray(a, float), np.asarray(b, float)
    return a + (b - a) * t
