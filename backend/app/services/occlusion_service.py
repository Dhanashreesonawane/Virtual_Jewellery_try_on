"""Heuristic, landmark-based occlusion. NOT depth-aware.
Swap in a segmentation model later by returning its mask from these functions."""
import cv2
import numpy as np


def hand_clip_mask(shape, hand_pts: np.ndarray, margin: float) -> np.ndarray:
    """Soft mask = hand convex hull grown by `margin` px. Keeps a ring on the hand."""
    mask = np.zeros(shape[:2], np.uint8)
    hull = cv2.convexHull(hand_pts.astype(np.int32))
    cv2.fillConvexPoly(mask, hull, 255)
    k = max(3, int(margin) | 1)
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    return cv2.GaussianBlur(mask, (5, 5), 0).astype(np.float32) / 255.0
