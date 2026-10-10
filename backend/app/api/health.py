from fastapi import APIRouter
from ..core.errors import ok
from ..database.mongodb import get_db, ping

router = APIRouter()


@router.get("/health")
def health():
    return ok({"status": "ok", "database": "mongodb" if get_db() is not None else "json-file",
               "database_ok": ping()})
