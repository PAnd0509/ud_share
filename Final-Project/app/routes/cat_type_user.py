# app/routes/cat_type_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.schemas.cat_type_user import CatTypeUserCreate, CatTypeUserOut, CatTypeUserUpdate

from app.crud.sql_crud import (
    create_cat_type_user,
    get_all_cat_type_users,
    get_cat_type_user_by_id,
    update_cat_type_user,
    delete_cat_type_user
)

router = APIRouter(prefix="/cat_type_users", tags=["CatTypeUser"])

@router.post("/", response_model=CatTypeUserOut)
def create_cat_user(cat: CatTypeUserCreate, db: Session = Depends(get_db)):
    return create_cat_type_user(db, cat)

@router.get("/", response_model=list[CatTypeUserOut])
def list_cat_users(db: Session = Depends(get_db)):
    return get_all_cat_type_users(db)

@router.get("/{cat_id}", response_model=CatTypeUserOut)
def get_cat_user(cat_id: int, db: Session = Depends(get_db)):
    cat = get_cat_type_user_by_id(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.put("/{cat_id}", response_model=CatTypeUserOut)
def update_cat_user(cat_id: int, cat_data: CatTypeUserUpdate, db: Session = Depends(get_db)):
    cat = update_cat_type_user(db, cat_id, cat_data)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.delete("/{cat_id}", response_model=CatTypeUserOut)
def delete_cat_user(cat_id: int, db: Session = Depends(get_db)):
    cat = delete_cat_type_user(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat
