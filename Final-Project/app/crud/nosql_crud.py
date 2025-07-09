from typing import List, Literal, Optional
from bson import ObjectId
from pymongo import ReturnDocument
from datetime import date

from app.db.mongo import get_db               
from app.models.nosql_models import FollowerDoc

COLLECTION_NAME = "follower"

# helpers internos
def _collection():
    return get_db()[COLLECTION_NAME]         

# Crear seguimiento

async def create_follower(data: FollowerDoc) -> FollowerDoc:
    follower_dict = data.dict(by_alias=True, exclude_none=True)
    result = await _collection().insert_one(follower_dict)
    follower_dict["_id"] = result.inserted_id
    return FollowerDoc(**follower_dict)


def get_all_followers(limit: int = 1000) -> list[FollowerDoc]:
    cursor = _col().find().limit(limit)
    return [FollowerDoc(**d) for d in cursor]

async def get_follower_by_id(follower_id: str) -> Optional[FollowerDoc]:
    if not ObjectId.is_valid(follower_id):
        return None
    doc = await _collection().find_one({"_id": ObjectId(follower_id)})
    return FollowerDoc(**doc) if doc else None

async def delete_follower(follower_id: str) -> bool:
    if not ObjectId.is_valid(follower_id):
        return False
    result = await _collection().delete_one({"_id": ObjectId(follower_id)})
    return result.deleted_count == 1

async def update_follower_status(
    follower_id: str, new_status: Literal["ON", "OFF"] = "OFF"
) -> Optional[FollowerDoc]:

    if not ObjectId.is_valid(follower_id):
        return None

    updated = await _collection().find_one_and_update(
        {"_id": ObjectId(follower_id)},
        {"$set": {"status": new_status}},
        return_document=ReturnDocument.AFTER,
    )
    return FollowerDoc(**updated) if updated else None
