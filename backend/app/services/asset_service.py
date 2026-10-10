"""Product photo -> normalized transparent RGBA PNG.

Background removal is colour-based: the background colour is estimated from the image
border and pixels close to it become transparent. It works for plain / studio backgrounds
(typical product shots). For busy backgrounds, swap make_transparent() for a segmentation
model (e.g. rembg) - the rest of the pipeline stays the same."""
import cv2
import numpy as np


def make_transparent(img: np.ndarray, tol: float = 40.0) -> np.ndarray:
    if img.ndim == 3 and img.shape[2] == 4 and img[..., 3].min() < 250:
        return img                                       # already has real transparency
    bgr = img[..., :3] if img.ndim == 3 else cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    border = np.concatenate([bgr[0], bgr[-1], bgr[:, 0], bgr[:, -1]])
    bg = np.median(border, axis=0)
    diff = np.linalg.norm(bgr.astype(np.float32) - bg, axis=2)
    mask = ((diff > tol) * 255).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    mask = cv2.GaussianBlur(cv2.erode(mask, np.ones((2, 2), np.uint8)), (3, 3), 0)
    return np.dstack([bgr, mask])


def crop_and_normalize(bgra: np.ndarray, max_side: int = 800, pad: int = 4) -> np.ndarray:
    ys, xs = np.where(bgra[..., 3] > 10)
    if len(xs) < 50:
        raise ValueError("no jewellery found after background removal")
    h, w = bgra.shape[:2]
    out = bgra[max(ys.min() - pad, 0):min(ys.max() + pad + 1, h), max(xs.min() - pad, 0):min(xs.max() + pad + 1, w)]
    s = max_side / max(out.shape[:2])
    return cv2.resize(out, None, fx=s, fy=s, interpolation=cv2.INTER_AREA) if s < 1 else out


def prepare_asset(img: np.ndarray) -> np.ndarray:
    return crop_and_normalize(make_transparent(img))


def make_thumbnail(bgra: np.ndarray, size: int = 256) -> np.ndarray:
    s = size / max(bgra.shape[:2])
    return cv2.resize(bgra, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
