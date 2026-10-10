"""Settings read from environment variables (see .env.example)."""
import os
from dataclasses import dataclass
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    origins: tuple = tuple(os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","))
    max_upload_bytes: int = int(float(os.getenv("MAX_UPLOAD_MB", "8")) * 1024 * 1024)
    max_side: int = int(os.getenv("MAX_IMAGE_SIDE", "1280"))
    data_dir: Path = BASE / "app" / "data"
    assets_dir: Path = BASE / "app" / "data" / "assets"
    outputs_dir: Path = BASE / "outputs"


settings = Settings()
settings.outputs_dir.mkdir(exist_ok=True)
settings.assets_dir.mkdir(parents=True, exist_ok=True)
