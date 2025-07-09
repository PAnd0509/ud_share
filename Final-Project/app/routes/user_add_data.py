# app/routes/user_add_data.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.schemas.user_add_data import (
    UserAddDataCreate, UserAddDataOut, UserAddDataUpdate
)
from app.crud.sql_crud import (
    create_user_add_data,
    get_user_add_data_by_id,
    get_user_add_data_by_user_id,
    update_user_add_data,
    delete_user_add_data
)

router = APIRouter(prefix="/user-add-data", tags=["UserAddData"])

@router.post("/", response_model=UserAddDataOut)
def create(data: UserAddDataCreate, db: Session = Depends(get_db)):
    result = create_user_add_data(db, data)
    if not result:
        raise HTTPException(status_code=400, detail="Data already exists for this user")
    return result

@router.get("/{record_id}", response_model=UserAddDataOut)
def get_by_id(record_id: int, db: Session = Depends(get_db)):
    record = get_user_add_data_by_id(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.get("/user/{user_id}", response_model=UserAddDataOut)
def get_by_user(user_id: int, db: Session = Depends(get_db)):
    record = get_user_add_data_by_user_id(db, user_id)
    if not record:
        raise HTTPException(status_code=404, detail="No additional data for this user")
    return record

@router.put("/{record_id}", response_model=UserAddDataOut)
def update(record_id: int, data: UserAddDataUpdate, db: Session = Depends(get_db)):
    record = update_user_add_data(db, record_id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.delete("/{record_id}", response_model=UserAddDataOut)
def delete(record_id: int, db: Session = Depends(get_db)):
    record = delete_user_add_data(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
