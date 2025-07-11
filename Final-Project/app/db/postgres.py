from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from app.config.settings import POSTGRES_URL

engine = create_engine(POSTGRES_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        