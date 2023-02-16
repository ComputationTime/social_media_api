from . import models
from .database import engine
from fastapi import FastAPI
from .routers import users, posts, authentication, votes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)
app.include_router(votes.router)
