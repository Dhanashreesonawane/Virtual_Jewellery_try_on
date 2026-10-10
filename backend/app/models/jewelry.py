from dataclasses import dataclass
import numpy as np


@dataclass
class Detection:
    pts: np.ndarray                 # (N,2) pixel coordinates
    score: float
    vis: np.ndarray | None = None   # per-landmark visibility (pose)


@dataclass
class Placement:
    """ROI for one jewelry piece: where, how big, how rotated."""
    center: tuple[float, float]     # anchor point in pixels
    width: float                    # target jewelry width in pixels
    rotation: float                 # OpenCV degrees (CCW positive)
    anchor_y: float                 # 0 = anchor is top of asset, 0.5 = middle
    confidence: float
    clip_pts: np.ndarray | None = None
