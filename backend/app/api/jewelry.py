from fastapi import APIRouter
from ..core.errors import ok
from ..database.repositories import jewelry_repo
from ..utils.validation import validate_category

router = APIRouter()
repo = jewelry_repo()


def _public(item):
    d = item.model_dump()
    d["thumbnail_url"] = "/" + item.thumbnail_path
    return d


@router.get("/jewelry")
@router.get("/jewellery")
def list_jewelry(category: str | None = None):
    if category:
        validate_category(category)
    return ok([_public(i) for i in repo.all(category)])


@router.get("/jewelry/{jewelry_id}")
@router.get("/jewellery/{jewelry_id}")
def get_jewelry(jewelry_id: str):
    return ok(_public(repo.get(jewelry_id)))
