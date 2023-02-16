from . import models
from .database import engine
from fastapi import FastAPI
from .routers import users, posts, authentication, votes

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)
app.include_router(votes.router)
