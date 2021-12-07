from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, utils 
from ..database import get_db

router = APIRouter(
    prefix='/api/users',
    tags=['Users']
)

# <---------------------------- create user ---------------------------------->
@router.post(
    "/create",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check whether email already exist
    x_email = db.query(models.User).filter(user.email == models.User.email).first()
    if x_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'This email has already registered',
        )

    # grnerate hash of given password
    hashed_password = utils.get_hash_from_str(user.password)
    user.password = hashed_password

    created_user = models.User(**user.dict())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


# <--------------------------- get all users ---------------------------------------->
@router.get("/get-all")
def get_all_users(db: Session = Depends(get_db)):
    user_list = db.query(models.User).all()
    return user_list

# <--------------------------- get user by id ---------------------------------------->
@router.get('/get/{user_id}', response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found',
        )
    
    return user