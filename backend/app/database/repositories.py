"""Collections: `jewellery` and `tryon_results`. Same interface as the JSON repositories."""
import time
import uuid
from ..core.errors import AppError
from ..services.repositories import JewelryRepository as JsonJewelry, ResultRepository as JsonResults, to_item
from .mongodb import get_db


class MongoJewelryRepository:
    def __init__(self, db):
        self.col = db["jewellery"]

    def all(self, category=None):
        q = {"active": {"$ne": False}}
        if category:
            q["category"] = category
        return [to_item(d) for d in self.col.find(q)]

    def get(self, jewelry_id):
        d = self.col.find_one({"_id": jewelry_id, "active": {"$ne": False}})
        if not d:
            raise AppError("JEWELRY_NOT_FOUND", "That jewellery item does not exist.", 404)
        return to_item(d)

    def upsert(self, doc):
        self.col.replace_one({"_id": doc["_id"]}, doc, upsert=True)


class MongoResultRepository:
    def __init__(self, db):
        self.col = db["tryon_results"]

    def all(self):
        return [{**{k: v for k, v in d.items() if k != "_id"}, "id": d["_id"]}
                for d in self.col.find().sort("saved_at", -1).limit(200)]

    def add(self, record):
        doc = {"_id": uuid.uuid4().hex[:12], "saved_at": time.time(), **record}
        self.col.insert_one(doc)
        return {**{k: v for k, v in doc.items() if k != "_id"}, "id": doc["_id"]}


def jewelry_repo():
    db = get_db()
    return MongoJewelryRepository(db) if db is not None else JsonJewelry()


def result_repo():
    db = get_db()
    return MongoResultRepository(db) if db is not None else JsonResults()
