from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime 

# the base class for Post
class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    # pass means its gonna use
    # all fields of its base class
    pass

"""
the class for the response body
what ever we return from the database
those will converted to this model
"""
class PostResponse(PostBase):
    id: int
    created_at: datetime

    # this snippet of code enable
    # the ability to convert to dictionary
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class LoginRequesat(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str

    class Config:
        orm_mode: True

class TokenData(BaseModel):
    id: Optional[str] = None
