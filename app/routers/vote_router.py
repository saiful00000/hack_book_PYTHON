from fastapi import FastAPI, status, APIRouter, Response, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils
from .. import oauth2

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.VoteRequest,
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):

    # fisrt of all we must check is the post exist or not
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == str(token_data.id), models.Vote.post_id == vote.post_id
    )

    vote_from_db = vote_query.first()

    if vote.direction == 1:
        # if the vote exists that means we already voted
        # to this post
        if vote_from_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Alrady voted to this post",
            )
        # if the vote is not already counted
        new_vote = models.Vote(user_id=token_data.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        # db.refresh(new_vote)
        return {"message": "Successful!"}
    else:
        # if vote not exist then we can not remove the vote
        if not vote_from_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not counted before, so can not remove vote",
            )

        vote_query.delete()
        db.commit()

        return {"message": "successfully deleted vote."}
