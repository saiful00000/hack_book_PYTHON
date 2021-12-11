from fastapi import FastAPI, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.constants import strings

from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login", response_model=schemas.TokenResponse)
def login(cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_from_db = db.query(models.User).filter(models.User.email == cred.username).first()

    # check existance
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email"
        )

    # match the password
    if not utils.verifyPassword(cred.password, user_from_db.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid password"
        )

    # generate a access token
    access_token = oauth2.create_access_token({strings.USER_ID: user_from_db.id})

    return {
        "message": "Successfully loged in.",
        "access_token": access_token,
        "token_type": "Bearer",
    }
