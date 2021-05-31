from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime

from .database import Base


# Create SQLAlchemy models from the Base class
class User(Base):
    __tablename__ = "users"

    # Create model attributes/columns
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

# Create SQLAlchemy models from the Base class
class Message(Base):
    __tablename__ = "messages"

    # Create model attributes/columns
    id = Column(Integer, primary_key=True, index=True)
    from_usr = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    to_usr = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    msg_content = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
