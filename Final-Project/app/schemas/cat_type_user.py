# app/schemas/cat_type_user.py
from pydantic import BaseModel

class CatTypeUserBase(BaseModel):
    type: str
    label: str
    description: str | None = None

class CatTypeUserCreate(CatTypeUserBase):
    pass

class CatTypeUserUpdate(BaseModel):
    type: str | None = None
    label: str | None = None
    description: str | None = None

class CatTypeUserOut(CatTypeUserBase):
    id: int

    class Config:
        orm_mode = True
