from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    msg_content: str
    from_usr: int


class MessageCreate(MessageBase):
    class Config:
        orm_mode = True


class Message(MessageBase):
    id: int
    to_usr: int
    date: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True