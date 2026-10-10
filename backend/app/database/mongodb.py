"""MongoDB connection (optional: without MONGO_URI the JSON-file repositories are used)."""
import os

_client = None


def get_db():
    global _client
    uri = os.getenv("MONGO_URI")
    if not uri:
        return None
    if _client is None:
        from pymongo import MongoClient
        _client = MongoClient(uri, serverSelectionTimeoutMS=2000)
    return _client[os.getenv("MONGO_DB", "jewellery_tryon")]


def ping() -> bool | None:
    """True/False for a configured MongoDB, None when MongoDB is not configured."""
    db = get_db()
    if db is None:
        return None
    try:
        db.client.admin.command("ping")
        return True
    except Exception:
        return False
