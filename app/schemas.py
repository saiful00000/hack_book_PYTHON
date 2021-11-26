from pydantic import BaseModel
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


# the class for the response body
# what ever we return from the database
# those will converted to this model
class PostResponse(PostBase):
    id: int
    created_at: datetime

    # this snippet of code enable
    # the ability to convert to dictionary
    class Config:
        orm_mode = True
