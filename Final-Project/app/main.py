from fastapi import FastAPI
from app.routes import users, posts

app = FastAPI()

app.include_router(users.router)
app.include_router(cat_type_user.router)
app.include_router(user.router)

