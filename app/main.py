from typing import Optional

from pydantic import BaseModel

from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

# create database and tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# # pydantic post model
class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


# # root
@app.get("/")
def root():
    return {"data": "Welcome to hackbook"}


# get all posts
@app.get("/api/posts")
def get_all_posts(db: Session = Depends(get_db)):
    post_list = db.query(models.Post).all()
    return post_list


# create a new post
@app.post("/api/create-post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get specific post by id
@app.get("/api/get-post/{post_id}")
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )
    
    return post
