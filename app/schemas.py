from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreated(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    published: bool = True
    pass

class Post(PostBase):
    id: int
    class config:
        orm_mode = True

class ResponsePost(Post):
    # owner: UserCreated
    id: int
    created_at: datetime
    class Config:
        from_attributes = True #orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

"""
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)

class PostWithVotesCount(BaseModel):
    Post: ResponsePost
    votes: int
"""