from fastapi import FastAPI

from . import models
from .database import engine

from .routers import user_router, post_router, auth_router, vote_router

# create database and tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(vote_router.router)


# root ---------------------------------------------------------------------
@app.get("/")
def root():
    return {"data": "Welcome to HackBook"}
