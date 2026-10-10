from typing import Optional
from pydantic import BaseModel


class JewelryItem(BaseModel):
    id: str
    name: str
    category: str
    asset_path: str
    thumbnail_path: str
    anchor_type: str
    default_scale: float = 1.0
    rotation_offset: float = 0.0
    x_offset: float = 0.0   # fraction of jewelry width
    y_offset: float = 0.0
    enabled: bool = True
    brand: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class FrameRequest(BaseModel):
    image: str                      # base64 or data URL
    jewelry_id: str
    category: str
    side: str = "both"              # earrings: left | right | both (image left/right)


class SaveResultRequest(BaseModel):
    image_url: str                  # must be a /outputs/<file> url returned by try-on
    jewelry_id: str
    category: str
    processing_time_ms: Optional[float] = None
