import base64
import cv2
import numpy as np
from ..core.config import settings
from ..core.errors import AppError
from .validation import is_jpeg_or_png


def decode_image(data: bytes) -> np.ndarray:
    """bytes -> BGR image, with validation."""
    if not data:
        raise AppError("EMPTY_UPLOAD", "The uploaded file is empty.")
    if len(data) > settings.max_upload_bytes:
        raise AppError("IMAGE_TOO_LARGE", "Image is too large.", 413)
    if not is_jpeg_or_png(data):
        raise AppError("UNSUPPORTED_FORMAT", "Only JPG and PNG images are supported.", 415)
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None or img.size == 0:
        raise AppError("INVALID_IMAGE", "The image could not be read.")
    return img


def decode_base64(text: str) -> np.ndarray:
    if "," in text[:100]:
        text = text.split(",", 1)[1]
    try:
        raw = base64.b64decode(text, validate=True)
    except Exception:
        raise AppError("INVALID_IMAGE", "Frame is not valid base64.")
    return decode_image(raw)


def normalize(img: np.ndarray, max_side: int | None = None) -> np.ndarray:
    """Shrink so the longest side <= max_side, keeping aspect ratio."""
    max_side = max_side or settings.max_side
    h, w = img.shape[:2]
    s = max_side / max(h, w)
    if s >= 1:
        return img
    return cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)


def denoise(img: np.ndarray) -> np.ndarray:
    return cv2.GaussianBlur(img, (3, 3), 0)


def to_rgb(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
