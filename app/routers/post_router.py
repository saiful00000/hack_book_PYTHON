from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])

# <----------------------------- get all posts --------------------------------------->
@router.get("/get-all", response_model=List[schemas.PostResponse])
def get_all_posts(
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    post_list = db.query(models.Post).all()
    return post_list


# <============================= create a new post ----------------------------------->
@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    print(f"token data = {token_data.dict()}")
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# <----------------------------get specific post by id ------------------------------->
@router.get("/get/{post_id}", response_model=schemas.PostResponse)
def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={post_id} not found",
        )

    return post


# <--------------------------- update a post by post id ------------------------------>
@router.put("/update/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
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


# <---------------------------- delete a specific post ------------------------------->
@router.delete("/delete/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
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
