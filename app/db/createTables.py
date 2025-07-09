from app.models.sql_models import Base
from app.db.postgres import engine
Base.metadata.create_all(bind=engine)
