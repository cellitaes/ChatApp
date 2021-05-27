from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from server import crud, models, schemas
from server.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chat")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=schemas.User)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.login_user(db, user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put('/users/status', response_model=schemas.User)
def update_user_status(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.update_user_status(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/status/{status}")
def get_users_by_status(status: str, db: Session = Depends(get_db)):
    if status.lower() == "active":
        return crud.get_users_by_status(db, True)
    elif status.lower() == "inactive":
        return crud.get_users_by_status(db, False)
    else:
        raise HTTPException(status_code=404, detail="Status not found")


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/message/", response_model=List[schemas.Message])
def read_all_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_all_messages(db, skip=skip, limit=limit)
    return messages


@app.post("/message/{receiver_id}/", response_model=schemas.Message)
def create_message_from_user(message: schemas.MessageCreate, receiver_id: int, db: Session = Depends(get_db)):
    return crud.create_message(db=db, message=message, receiver_id=receiver_id)


@app.get("/message/{receiver_id}/{sender_id}/", response_model=List[schemas.Message])
def read_messages_to_user_from(receiver_id: int, sender_id: int, skip: int = 0, limit: int = 100,
                               db: Session = Depends(get_db)):
    messages = crud.get_messages_to_user_from(db, receiver_id=receiver_id, sender_id=sender_id, skip=skip,
                                              limit=limit)
    return messages


@app.get("/message/{receiver_id}/{sender_id}/{from_date}", response_model=List[schemas.Message])
def read_messages_to_user_from_date(receiver_id: int, sender_id: int, from_date: datetime, skip: int = 0,
                                    limit: int = 100, db: Session = Depends(get_db)):
    if sender_id == 0:
        messages = crud.get_messages_to_general(db, from_date)
    else:
        messages = crud.get_messages_to_user_from_date(db, receiver_id=receiver_id, sender_id=sender_id, date=from_date,
                                                       skip=skip, limit=limit)
    return messages


@app.delete("/message/{message_id}")
def delete_message_by_id(message_id: int, db: Session = Depends(get_db)):
    if crud.delete_message_by_id(db, message_id):
        return status.HTTP_202_ACCEPTED
    return status.HTTP_204_NO_CONTENT
