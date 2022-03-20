from typing import List
from fastapi import APIRouter, Depends, File, Form, Response, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# <--------------------------- upload profile image --------------------------------->
@router.put("/upload/profile-picture")
def upload_profile_picture(
    profile_picture: bytes = File(...),
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    new_query = db.query(models.User).filter(token_data.id == models.User.id)
    x_user_data = new_query.first()
    
    # check whther user exist or not
    if not x_user_data:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    print(f'user id = {x_user_data.id} token_id = {token_data.id}')
    
    # recheck whther user is the valid user
    if str(x_user_data.id) != token_data.id:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='The request is forbiden',
        )
    
    return {'file_size': len(profile_picture)}




# <--------------------------- get all users ---------------------------------------->
@router.get("/get-all", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()
    return user_list


# <--------------------------- get user by id ---------------------------------------->
@router.get("/get/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )

    return user
