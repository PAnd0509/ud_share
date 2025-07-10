from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from app.crud.nosql_crud import (
    create_follower,
    get_all_followers,
    get_follower_by_id,
    delete_follower,
    update_follower_status,
)
from app.models.nosql_models import FollowerDoc

router = APIRouter(prefix="/followers", tags=["Followers"])

@router.get("")
async def api_list_followers():
    return await run_in_threadpool(get_all_followers)

@router.post("", response_model=FollowerDoc, status_code=201)
async def api_create_follower(follower: FollowerDoc):
    return await create_follower(follower)

@router.get("/{fid}", response_model=FollowerDoc)
async def api_get_follower(fid: str):
    doc = await get_follower_by_id(fid)
    if doc is None:
        raise HTTPException(404, "Follower not found")
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
