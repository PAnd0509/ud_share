from typing import List, Literal, Optional
from bson import ObjectId
from pymongo import ReturnDocument
from datetime import datetime, date
from fastapi.concurrency import run_in_threadpool
from fastapi import HTTPException
from app.db.mongo import get_db               
from app.models.nosql_models import FollowerDoc

COLLECTION_NAME = "follower"

# helpers internos
def _collection():
    return get_db()[COLLECTION_NAME]         

# Crear seguimiento

async def create_follower(follower: FollowerDoc):
    collection = _collection()

    # Verificación previa
    exists = await run_in_threadpool(lambda: collection.find_one({
        "follower_user_id": follower.follower_user_id,
        "followed_user_id": follower.followed_user_id
    }))
    if exists:
        raise HTTPException(status_code=409, detail="Follower already exists")
    
    follower_dict = follower.dict(exclude_unset=True, exclude_none=True)

    if "date_begin_follow" not in follower_dict:
        follower_dict["date_begin_follow"] = datetime.utcnow()
    else:
        # Si vino como date (de Pydantic), conviértelo a datetime
        if isinstance(follower_dict["date_begin_follow"], date):
            follower_dict["date_begin_follow"] = datetime.combine(follower_dict["date_begin_follow"], datetime.min.time())

    result = await run_in_threadpool(lambda: collection.insert_one(follower_dict))
    follower.id = str(result.inserted_id)
    return follower


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
