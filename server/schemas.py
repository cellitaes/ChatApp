from dataclasses import Field

from pydantic import BaseModel
from datetime import datetime

# Create the Pydantic models
# Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model

class MessageBase(BaseModel):
    msg_content: str
    from_usr: int


class MessageCreate(MessageBase):
    class Config:
        orm_mode = True


class Message(MessageBase):
    # Create Pydantic models / schemas for reading / returning
    id: int
    to_usr: int
    date: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    password: str


class UserBan(BaseModel):
    id: int
    is_banned: bool

    class Config:
        orm_mode = True


class User(UserBase):
    # Create Pydantic models / schemas for reading / returning
    id: int
    is_active: bool
    is_banned: bool

    class Config:
        orm_mode = True
