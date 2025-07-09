# app/routes/post.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.db.postgres import get_db
from app.schemas.post import (
    PostCreate, PostUpdate, PostOut,
    AttachedMultimediaCreate, AttachedMultimediaUpdate, AttachedMultimediaOut
)
from app.crud.sql_crud import (
    create_post, get_post_by_id, get_all_posts, update_post, delete_post,
    create_attachment, get_attachment_by_id, get_all_attachments,
    update_attachment, delete_attachment
)

router = APIRouter(prefix="/posts", tags=["Posts"])

# -------- POST --------

@router.post("/", response_model=PostOut)
def create(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)

@router.get("/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostOut)
def update(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):
    post = update_post(db, post_id, data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}", response_model=PostOut)
def delete(post_id: int, db: Session = Depends(get_db)):
    post = delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# -------- ATTACHMENTS --------

@router.post("/attachments/", response_model=AttachedMultimediaOut)
def create_media(data: AttachedMultimediaCreate, db: Session = Depends(get_db)):
    return create_attachment(db, data)

@router.get("/attachments/", response_model=list[AttachedMultimediaOut])
def list_media(db: Session = Depends(get_db)):
    return get_all_attachments(db)

@router.get("/attachments/{media_id}", response_model=AttachedMultimediaOut)
def get_media(media_id: int, db: Session = Depends(get_db)):
    media = get_attachment_by_id(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@router.put("/attachments/{media_id}", response_model=AttachedMultimediaOut)
def update_media(media_id: int, data: AttachedMultimediaUpdate, db: Session = Depends(get_db)):
    media = update_attachment(db, media_id, data)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

@router.delete("/attachments/{media_id}", response_model=AttachedMultimediaOut)
def delete_media(media_id: int, db: Session = Depends(get_db)):
    media = delete_attachment(db, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")
    return media
