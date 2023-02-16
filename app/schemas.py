from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class BaseUser(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserPost(BaseUser):
    pass


class UserReturn(BaseModel):
    user_id: int
    username: str

    class Config:
        orm_mode = True


class UserPrivate(UserReturn):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostPost(PostBase):
    pass


class PostPut(PostBase):
    pass


class PostReturn(PostBase):
    created_at: datetime
    user_id: int
    post_id: int
    owner: UserReturn

    class Config:
        orm_mode = True


class PostFullReturn(BaseModel):
    Post: PostReturn
    likes: int
    dislikes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=-1)
