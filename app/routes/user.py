from fastapi import APIRouter, Depends
from app.db.postgres import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")

@router.get("/")
def get_users():
    # lógica para listar usuarios desde PostgreSQL
    return {"message": "List of users"}
