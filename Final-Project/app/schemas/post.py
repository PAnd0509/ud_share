# app/schemas/post.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# -------- POST --------

class PostBase(BaseModel):
    text_post: str = Field(..., max_length=800)
    fk_visibility_type: Optional[int] = None
    fk_user_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    text_post: Optional[str] = None
    fk_visibility_type: Optional[int] = None

class PostOut(PostBase):
    id: int
    date_post: date

    class Config:
        orm_mode = True

# -------- ATTACHED MULTIMEDIA --------

class AttachedMultimediaBase(BaseModel):
    name: str
    format: str
    size: Optional[str] = None
    characteristics: Optional[str] = None
    fk_post_id: Optional[int] = None
    fk_comment_id: Optional[int] = None

class AttachedMultimediaCreate(AttachedMultimediaBase):
    pass

class AttachedMultimediaUpdate(BaseModel):
    name: Optional[str] = None
    format: Optional[str] = None
    size: Optional[str] = None
    characteristics: Optional[str] = None

class AttachedMultimediaOut(AttachedMultimediaBase):
    id: int

    class Config:
        orm_mode = True
