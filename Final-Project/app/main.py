from fastapi import FastAPI
from app.routes import users, cat_type_user, user, user_add_data, follower, post, comment   

app = FastAPI()

app.include_router(users.router)
app.include_router(cat_type_user.router)
app.include_router(user.router)
app.include_router(user_add_data.router)    
app.include_router(follower.router)
app.include_router(post.router)
app.include_router(comment.router)

