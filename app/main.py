from typing import Optional, List

from pydantic import BaseModel

from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from . import schemas
from . import models
from . import utils
from .database import engine, get_db

from .routers import user_router, post_router

# create database and tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)
app.include_router(post_router.router)

# root ---------------------------------------------------------------------
@app.get("/")
def root():
    return {"data": "Welcome to HackBook"}
