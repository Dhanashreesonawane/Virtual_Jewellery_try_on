from ..core.constants import CATEGORIES
from ..core.errors import AppError


def validate_category(category: str) -> str:
    if category not in CATEGORIES:
        raise AppError("INVALID_CATEGORY", f"Category must be one of: {', '.join(CATEGORIES)}.")
    return category


def is_jpeg_or_png(data: bytes) -> bool:
    return (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n"
            or (data[:4] == b"RIFF" and data[8:12] == b"WEBP"))
