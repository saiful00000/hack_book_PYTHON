from distutils import file_util
from fileinput import filename
from typing import Dict, List
from django.urls import path
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Response,
    UploadFile,
    status,
    HTTPException,
    Request,
)
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db

from ..my_utils import file_utils

router = APIRouter(prefix="/users", tags=["Users"])

# <--------------------------- upload profile image --------------------------------->
@router.put("/upload/profile-picture")
async def upload_profile_picture(
    request: Request,
    profile_picture: UploadFile = File(...),
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    # check the MIME type of the file and validate that the file is a image file
    if profile_picture.content_type != 'image/jpeg':
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Provide a valid image file'
        )

    new_query = db.query(models.User).filter(token_data.id == models.User.id)
    x_user_data: models.User = new_query.first()

    # check whther user exist or not
    if not x_user_data:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # print(f"user id = {x_user_data.id} token_id = {token_data.id}")

    # recheck whther user is the valid user
    if str(x_user_data.id) != token_data.id:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The request is forbiden",
        )

    mfile_info: Dict = file_utils.save_profile_picture(profile_picture, user_id=token_data.id)
    print(f'file information = {mfile_info}')

    image_url: str = request.url_for('profile_pictures', path=mfile_info['file_name'])

    # here save the image url to databse
    # print(f'x user data = {dict(x_user_data)}')
    user_map: Dict = {
        "profile_picture": image_url,
    }
    new_query.update(user_map)
    db.commit()

    return {"profile_pictures": image_url}


# <--------------------------- get all users ---------------------------------------->
@router.get("/get-all", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()
    return user_list


# <--------------------------- get user by id ---------------------------------------->
@router.get(
    "/get/{user_id}",
    response_model=schemas.UserResponse,
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )

    return user
