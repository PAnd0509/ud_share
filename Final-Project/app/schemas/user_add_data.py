# app/schemas/user_add_data.py
from pydantic import BaseModel, Field
from typing import Optional

class UserAddDataBase(BaseModel):
    profile_description: Optional[str] = Field(default=None, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=10)
    social_media: Optional[str] = Field(default=None, max_length=100)
    fk_user_id: int

class UserAddDataCreate(UserAddDataBase):
    pass

class UserAddDataUpdate(BaseModel):
    profile_description: Optional[str] = None
    phone: Optional[str] = None
    social_media: Optional[str] = None

class UserAddDataOut(UserAddDataBase):
    id: int

    class Config:
        orm_mode = True
