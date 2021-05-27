from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_usr = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    to_usr = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    msg_content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
