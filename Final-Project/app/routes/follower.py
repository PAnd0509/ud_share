# app/routes/follower.py
from fastapi import APIRouter, HTTPException
from app.models.follower_doc import FollowerDoc
from app.crud.nosql_crud import (
    create_follower, get_all_followers,
    get_follower_by_id, delete_follower, update_follower_status
)

router = APIRouter(prefix="/followers", tags=["Followers"])

@router.post("/", response_model=FollowerDoc)
async def create_follower_route(data: FollowerDoc):
    try:
        return await create_follower(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[FollowerDoc])
async def list_followers():
    return await get_all_followers()

@router.get("/{follower_id}", response_model=FollowerDoc)
async def get_follower(follower_id: str):
    doc = await get_follower_by_id(follower_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Follower not found")
    return doc

@router.delete("/{follower_id}")
async def delete_follower_route(follower_id: str):
    success = await delete_follower(follower_id)
    if not success:
        raise HTTPException(status_code=404, detail="Follower not found")
    return {"message": "Deleted successfully"}

@router.put("/{follower_id}/status/{status}", response_model=FollowerDoc)
async def update_status(follower_id: str, status: str):
    if status not in ("ON", "OFF"):
        raise HTTPException(status_code=400, detail="Invalid status")
    updated = await update_follower_status(follower_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Follower not found")
    return updated
