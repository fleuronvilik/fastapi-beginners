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

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class ResponsePost(Post):
    owner: UserCreated
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class PostWithVotesCount(BaseModel):
    Post: ResponsePost
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)  