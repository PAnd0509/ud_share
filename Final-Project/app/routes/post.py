# app/routes/post.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.schemas.post import (
    PostCreate, PostUpdate, PostOut,
    AttachedMultimediaCreate, AttachedMultimediaUpdate, AttachedMultimediaOut
)
from app.crud.sql_crud import (
    create_post, get_post_by_id, get_all_posts, update_post, delete_post
    #create_attachment, get_attachment_by_id, get_all_attachments,
    #update_attachment, delete_attachment
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
