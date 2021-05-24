from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.schema import CheckConstraint

from server.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    # messages = relationship("Message", back_populates="owner")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_usr = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    to_usr = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    msg_content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    is_read = Column(Boolean, nullable=False)

    # owner = relationship("User", back_populates="messages")