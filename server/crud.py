from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime

from server import models, schemas


def get_user(db: Session, user_id: int):
    """
    query that retrieves from the database of the user with the given id
    :param db: the database being searched
    :param user_id: the id of the searched user
    :return: found user
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    """
    query that retrieves from the database of the user with the given login
    :param db: the database being searched
    :param login: the login of the searched user
    :return: found user
    """
    return db.query(models.User).filter(models.User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    query that returns all users in the database
    :param db: the database being searched
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :return: All users from database
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    query that adds a new user to the database
    :param db: the database being searched
    :param user: new user to be added to the database
    :return: added user
    """
    password = user.password
    db_user = models.User(login=user.login, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_messages_to_user(db: Session, receiver_id: int, skip: int = 0, limit: int = 100):
    """
    query that finds all messages that have been received by a user with a given id
    :param db: the database being searched
    :param receiver_id: id of the user who received the message
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :return: all messages received by the user with the given id
    """
    return db.query(models.Message).filter(models.Message.to_usr == receiver_id).offset(skip).limit(limit).all()


def get_messages_to_user_from(db: Session, receiver_id: int, sender_id: int, skip: int = 0, limit: int = 100):
    """
    query that finds all messages that have been sent by a user with a given id to a user with a given id
    :param db: the database being searched
    :param receiver_id: id of the user who received the message
    :param sender_id: id of the user who sent the message
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :return: all messages that have been sent by a user with a given id to a user with a given id
    """
    return db.query(models.Message) \
        .filter(or_(and_(models.Message.to_usr == receiver_id, models.Message.from_usr == sender_id),
                    and_(models.Message.to_usr == sender_id, models.Message.from_usr == receiver_id))) \
        .order_by(models.Message.date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_messages_to_general(db: Session, date: datetime, skip: int = 0, limit: int = 100):
    """
    a query that finds all messages sent in chat 'general' since the given date
    :param db: the database being searched
    :param date: date from which messages are searched for
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :return: all messages sent in chat 'general' since the given date
    """
    return db.query(models.Message) \
        .filter(models.Message.to_usr == 0, models.Message.date > date) \
        .order_by(models.Message.date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_messages_to_user_from_date(db: Session, receiver_id: int, date: datetime, sender_id: int, skip: int = 0,
                                   limit: int = 100):
    """
    query that searches for all messages sent by a user with a given id to a user with a given id from a given date
    :param db: the database being searched
    :param receiver_id: id of the user who received the message
    :param date: date from which messages are searched for
    :param sender_id: id of the user who sent the message
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :return: all messages sent by a user with a given id to a user with a given id from a given date
    """
    return db.query(models.Message) \
        .filter(and_(or_(and_(models.Message.to_usr == receiver_id, models.Message.from_usr == sender_id),
                         and_(models.Message.to_usr == sender_id, models.Message.from_usr == receiver_id)),
                     models.Message.date > date)) \
        .order_by(models.Message.date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def get_all_messages(db: Session, skip: int = 0, limit: int = 100):
    """
    query that returns all sent messages
    :param db: the database being searched
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :return: all sent messages
    """
    return db.query(models.Message).offset(skip).limit(limit).all()


def create_message(db: Session, message: schemas.MessageCreate, receiver_id: int):
    """
    query that adds a new message to the database
    :param db: the database being searched
    :param message: message sent to the user
    :param receiver_id: id of the user who received the message
    :return: added message
    """
    db_message = models.Message(**message.dict(), date=datetime.now(), to_usr=receiver_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_user_status(db: Session, user: schemas.User):
    """
    query that changes the user's status (is_active)
    :param db: the database being searched
    :param user: the user whose status is to be changed
    :return: searched user
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_active = user.is_active
        db.commit()
        db.refresh(db_user)
    return db_user


def update_user_status_ban(db: Session, user: schemas.UserBan):
    """
    query that changes the user's status (is_banned)
    :param db: the database being searched
    :param user: the user whose status is to be changed
    :return: searched user
    """
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user:
        db_user.is_banned = user.is_banned
        db.commit()
        db.refresh(db_user)
    return db_user


def login_user(db: Session, user: schemas.UserCreate):
    """
    query that checks if a given user exists in the database
    :param db: the database being searched
    :param user: the user to log in
    :return: searched user or None if user is not found
    """
    db_user = db.query(models.User).filter(models.User.login == user.login).filter(
        models.User.password == user.password).first()
    if db_user:
        return db_user
    return None


def delete_message_by_id(db: Session, message_id: int):
    """
    query that removes the message with the given id from the database
    :param db: the database being searched
    :param message_id: message with the given id
    :return: confirmation that the operation was successful
    """
    db_message = db.query(models.Message).get(message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
        return True
    return False


def get_users_by_status(db: Session, status: bool):
    """
    a query that will find all users with a given status
    :param db: the database being searched
    :param status: status of searched users
    :return: all users with a given status
    """
    db_users = db.query(models.User).filter(models.User.is_active == status).all()
    return db_users
