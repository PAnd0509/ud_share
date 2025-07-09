# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserBase(BaseModel):
    nickname: str = Field(max_length=10)
    name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    birth_date: date
    email: EmailStr
    password: str = Field(max_length=60)  # hashed (opcionalmente)
    profile_image: str | None = None
    fk_type_user: int

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    nickname: str | None = Field(default=None, max_length=10)
    name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    birth_date: date | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, max_length=60)
    profile_image: str | None = None
    fk_type_user: int | None = None

class UserOut(UserBase):
    id: int
    date_create: date

    class Config:
        orm_mode = True
