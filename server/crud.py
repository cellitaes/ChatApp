from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from . import models, schemas
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    password = user.password
    db_user = models.User(login=user.login, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_messages_to_user(db: Session, receiver_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(models.Message.to_usr == receiver_id).offset(skip).limit(limit).all()


def get_messages_to_user_from(db: Session, receiver_id: int, sender_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message) \
        .filter(or_(and_(models.Message.to_usr == receiver_id, models.Message.from_usr == sender_id),
                    and_(models.Message.to_usr == sender_id, models.Message.from_usr == receiver_id))) \
        .order_by(models.Message.date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_messages_to_general(db: Session, date: datetime, skip: int = 0, limit: int = 100):
    return db.query(models.Message) \
        .filter(models.Message.to_usr == 0, models.Message.date > date) \
        .order_by(models.Message.date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_messages_to_user_from_date(db: Session, receiver_id: int, date: datetime, sender_id: int, skip: int = 0,
                                   limit: int = 100):
    return db.query(models.Message) \
        .filter(and_(or_(and_(models.Message.to_usr == receiver_id, models.Message.from_usr == sender_id),
                         and_(models.Message.to_usr == sender_id, models.Message.from_usr == receiver_id)),
                     models.Message.date > date)) \
        .order_by(models.Message.date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_all_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Message).offset(skip).limit(limit).all()


def create_message(db: Session, message: schemas.MessageCreate, receiver_id: int):
    db_message = models.Message(**message.dict(), date=datetime.now(), to_usr=receiver_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_user_status(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_active = user.is_active
        db.commit()
        db.refresh(db_user)
    return db_user


def login_user(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.login == user.login).filter(
        models.User.password == user.password).first()
    if db_user:
        return db_user
    return None


def delete_message_by_id(db: Session, message_id: int):
    db_message = db.query(models.Message).get(message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
        return True
    return False


def get_users_by_status(db: Session, status: bool):
    db_users = db.query(models.User).filter(models.User.is_active == status).all()
    return db_users
