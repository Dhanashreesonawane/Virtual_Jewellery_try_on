from fastapi import APIRouter, File, Form, UploadFile
from starlette.concurrency import run_in_threadpool
from ..core.constants import ALLOWED_TYPES
from ..core.errors import AppError, ok
from ..models.schemas import FrameRequest
from ..database.repositories import jewelry_repo
from ..services.tryon_service import run_tryon
from ..utils.image_utils import decode_base64, decode_image
from ..utils.validation import validate_category

router = APIRouter()
repo = jewelry_repo()


@router.post("/tryon/image")
async def tryon_image(image: UploadFile = File(...), jewelry_id: str = Form(...),
                      category: str = Form(...), side: str = Form("both"),
                      denoise: bool = Form(False), max_side: int | None = Form(None)):
    if image.content_type not in ALLOWED_TYPES:
        raise AppError("UNSUPPORTED_FORMAT", "Only JPG and PNG images are supported.", 415)
    validate_category(category)
    img = decode_image(await image.read())
    item = repo.get(jewelry_id)
    return ok(await run_in_threadpool(run_tryon, img, item, category, side, denoise, max_side))


@router.post("/tryon/frame")
async def tryon_frame(req: FrameRequest):
    validate_category(req.category)
    img = decode_base64(req.image)
    item = repo.get(req.jewelry_id)
    return ok(await run_in_threadpool(run_tryon, img, item, req.category, req.side))
