# app/crud/nosql_crud.py
from app.config.db.mongo import mongo_db
from app.models.follower_doc import FollowerDoc
from bson import ObjectId
from pymongo import ReturnDocument

COLLECTION_NAME = "follower"

# Crear seguimiento
async def create_follower(data: FollowerDoc) -> FollowerDoc:
    follower_dict = data.dict(by_alias=True)
    result = await mongo_db[COLLECTION_NAME].insert_one(follower_dict)
    follower_dict["_id"] = result.inserted_id
    return FollowerDoc(**follower_dict)

# Obtener todos
async def get_all_followers() -> list[FollowerDoc]:
    followers = await mongo_db[COLLECTION_NAME].find().to_list(1000)
    return [FollowerDoc(**doc) for doc in followers]

# Obtener por ID
async def get_follower_by_id(follower_id: str) -> FollowerDoc | None:
    doc = await mongo_db[COLLECTION_NAME].find_one({"_id": ObjectId(follower_id)})
    return FollowerDoc(**doc) if doc else None

# Eliminar
async def delete_follower(follower_id: str) -> bool:
    result = await mongo_db[COLLECTION_NAME].delete_one({"_id": ObjectId(follower_id)})
    return result.deleted_count == 1

# Actualizar estado (ejemplo: OFF)
async def update_follower_status(follower_id: str, new_status: str = "OFF") -> FollowerDoc | None:
    updated = await mongo_db[COLLECTION_NAME].find_one_and_update(
        {"_id": ObjectId(follower_id)},
        {"$set": {"status": new_status}},
        return_document=ReturnDocument.AFTER
    )
    return FollowerDoc(**updated) if updated else None
