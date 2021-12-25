from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import schemas, models, utils, oauth2
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])

# <----------------------------- get all posts --------------------------------------->
@router.get("/get-all", response_model=List[schemas.PostWithVoteResponse])
# @router.get("/get-all")
def get_all_posts(
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    print(f"token data from get all posts {token_data}")
    # post_list = db.query(models.Post).all()
    post_list = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True,
        )
        .group_by(models.Post.id)
        .all()
    )

    return post_list


# <------------------------------ Get My all posts ------------------------------------>
@router.get("/get-my-all", response_model=List[schemas.PostWithVoteResponse])
def get_my_all_posts(
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
    limit: int = None,
):
    if limit:
        # excecute when user send the limit by query parameter
        # m_posts_list = (
        #     db.query(models.Post,)
        #     .filter(str(token_data.id) == models.Post.woner_id)
        #     .limit(limit)
        #     .all()
        # )
        m_post_list = (
            db.query(
                models.Post,
                func.count(models.Vote.post_id).label("votes"),
            )
            .join(
                models.Vote,
                models.Vote.post_id == models.Post.id,
                isouter=True,
            )
            .group_by(models.Post.id)
            .filter(models.Post.woner_id == str(token_data.id))
            .limit(limit)
            .all()
        )
    else:
        # get all posts there isno limit
        # m_posts_list = (
        #     db.query(models.Post)
        #     .filter(str(token_data.id) == models.Post.woner_id)
        #     .all()
        # )
        m_post_list = (
            db.query(
                models.Post,
                func.count(models.Vote.post_id).label("votes"),
            )
            .join(
                models.Vote,
                models.Vote.post_id == models.Post.id,
                isouter=True,
            )
            .group_by(models.Post.id)
            .filter(models.Post.woner_id == str(token_data.id))
            .all()
        )

    return m_post_list


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

    post_dict = post.dict()
    post_dict["woner_id"] = token_data.id
    print(f"token data = {token_data.dict()}")
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# <---------------------------- get specific post by id ------------------------------->
@router.get("/get/{post_id}", response_model=schemas.PostWithVoteResponse)
def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # post = db.query(models.Post).filter(models.Post.id == post_id).first()
    post = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes"),
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True,
        )
        .group_by(models.Post.id)
        .filter(models.Post.id == post_id)
        .first()
    )

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

    if xPost.woner_id != int(token_data.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The post you are trying to edit, its not belongs to you",
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

    if deletedPost.woner_id != int(token_data.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The post you are trying to delete its not belongs to you",
        )

    delete_query.delete()
    db.commit()

    return {"message": "Post deleted"}
