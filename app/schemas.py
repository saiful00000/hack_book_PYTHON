from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint


"""
This group of pydantic model sare foe 
authentication related and define auth
related request body and response schemas
"""


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


"""
This group of pydantic models are defination of all post related
schemas
"""
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
those will converted to this model"""


class PostResponse(PostBase):
    id: int
    woner_id: int
    created_at: datetime
    woner: UserResponse

    # this snippet of code enable
    # the ability to convert to dictionary
    class Config:
        orm_mode = True

class PostWithVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


"""
the class represent the request body
of make vote api
"""


class VoteRequest(BaseModel):
    post_id: int
    # this field represent whether the vote is
    # an up vote or down vote
    direction: conint(le=1)
