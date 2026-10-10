"""Alpha-preserving rendering and compositing."""
import cv2
import numpy as np
from .alignment_service import create_affine_matrix


def premultiply(bgra: np.ndarray) -> np.ndarray:
    out = bgra.astype(np.float32)
    out[..., :3] *= out[..., 3:4] / 255.0
    return out


def render_jewelry(bgra: np.ndarray, scale: float, rotation: float) -> np.ndarray:
    """Scale + rotate a BGRA asset onto an enlarged canvas. Returns premultiplied float32.
    Premultiplying first avoids dark fringes on transparent edges."""
    h, w = bgra.shape[:2]
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    interp = cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC
    img = premultiply(cv2.resize(bgra, (nw, nh), interpolation=interp))
    M = create_affine_matrix((nw / 2, nh / 2), rotation)
    c, s = abs(M[0, 0]), abs(M[0, 1])
    bw, bh = int(nh * s + nw * c), int(nh * c + nw * s)
    M[0, 2] += bw / 2 - nw / 2
    M[1, 2] += bh / 2 - nh / 2
    return cv2.warpAffine(img, M, (bw, bh), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def composite_jewelry(background: np.ndarray, jewelry: np.ndarray,
                      mask: np.ndarray | None, position: tuple[int, int]) -> np.ndarray:
    """Blend premultiplied BGRA `jewelry` onto BGR `background` at top-left `position`.
    `mask` (float 0..1, background-sized) limits where jewelry may show. Edits in place."""
    x, y = position
    bh, bw = background.shape[:2]
    jh, jw = jewelry.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + jw, bw), min(y + jh, bh)
    if x1 <= x0 or y1 <= y0:
        return background
    fg = jewelry[y0 - y:y1 - y, x0 - x:x1 - x]
    if mask is not None:
        fg = fg * mask[y0:y1, x0:x1, None]
    alpha = fg[..., 3:4] / 255.0
    roi = background[y0:y1, x0:x1].astype(np.float32)
    background[y0:y1, x0:x1] = np.clip(fg[..., :3] + roi * (1 - alpha), 0, 255).astype(np.uint8)
    return background
