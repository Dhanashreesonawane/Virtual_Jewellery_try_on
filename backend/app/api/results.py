from pathlib import PurePosixPath
from fastapi import APIRouter
from ..core.config import settings
from ..core.errors import AppError, ok
from ..models.schemas import SaveResultRequest
from ..database.repositories import result_repo

router = APIRouter()
repo = result_repo()


@router.post("/results")
def save_result(req: SaveResultRequest):
    p = PurePosixPath(req.image_url)
    name = p.name
    if p.parent != PurePosixPath("/outputs") or not name.endswith(".jpg") \
            or not (settings.outputs_dir / name).is_file():
        raise AppError("INVALID_RESULT", "Only generated try-on images can be saved.")
    return ok(repo.add({"image_url": f"/outputs/{name}", "jewelry_id": req.jewelry_id,
                        "category": req.category, "processing_time_ms": req.processing_time_ms}))


@router.get("/results")
def list_results():
    return ok(repo.all())
