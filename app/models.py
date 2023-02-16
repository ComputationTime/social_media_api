from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from functools import partial

RequiredColumn = partial(Column, nullable=False)


class Post(Base):
    __tablename__ = "posts"

    post_id = RequiredColumn(Integer, primary_key=True)
    title = RequiredColumn(String)
    content = RequiredColumn(String)
    published = RequiredColumn(Boolean, server_default='TRUE')
    created_at = RequiredColumn(
        TIMESTAMP(timezone=True), server_default=text('now()'))
    user_id = RequiredColumn(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"))
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    user_id = RequiredColumn(Integer, primary_key=True)
    username = RequiredColumn(String, unique=True)
    password = RequiredColumn(String)
    email = RequiredColumn(String, unique=True)
    created_at = RequiredColumn(
        TIMESTAMP(timezone=True), server_default=text('now()'))


class Vote(Base):
    __tablename__ = "likes"

    user_id = RequiredColumn(Integer, ForeignKey(
        "users.user_id", ondelete="CASCADE"), primary_key=True)
    post_id = RequiredColumn(Integer, ForeignKey(
        "posts.post_id", ondelete="CASCADE"), primary_key=True)
    dir = RequiredColumn(Integer)
