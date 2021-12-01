from typing import Optional, List

from pydantic import BaseModel

from fastapi import FastAPI, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from . import schemas
from . import models
from .database import engine, get_db

# create database and tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# root ---------------------------------------------------------------------
@app.get("/")
def root():
    return {"data": "Welcome to hackbook"}


# <-------------------------------User-------------------------------------->
@app.post("/api/create-user", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@app.get('/api/get-users')
def get_all_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()
    return user_list

# <-------------------------------Post----------------------------------------->
# get all posts ------------------------------------------------------------
@app.get("/api/posts", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    post_list = db.query(models.Post).all()
    return post_list


# create a new post --------------------------------------------------------
@app.post(
    "/api/create-post",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get specific post by id --------------------------------------------------
@app.get("/api/get-post/{post_id}", response_model=schemas.PostResponse)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )

    return post


# update a post by post id -------------------------------------------------
@app.put("/api/update-post/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    update_query = db.query(models.Post).filter(models.Post.id == post_id)
    xPost = update_query.first()
    if not xPost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )

    update_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return update_query.first()


# delete a specific post ---------------------------------------------------
@app.delete("/api/delete/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    delete_query = db.query(models.Post).filter(models.Post.id == post_id)
    deletedPost = delete_query.first()

    if not deletedPost:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )

    delete_query.delete()
    db.commit()

    return {"message": "Post deleted"}



