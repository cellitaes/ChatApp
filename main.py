from typing import List

from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from datetime import datetime

from server import crud, models, schemas
from server.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chat")


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = dict()

    async def connect(self, websocket: WebSocket, client_id):
        """
        connect user to chat
        :param websocket: connection information
        :param client_id: id client that connects
        :return:
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket
        await self.broadcast(f"status")

    async def disconnect(self, client_id):
        """
        disconnect user from chat
        :param client_id: id client that disconnects
        :return:
        """
        self.active_connections.pop(client_id)
        await self.broadcast(f"status")

    async def send_personal_message(self, message: str, client_id):
        """
        send personal message to user with given id
        :param message: message to be sent
        :param client_id: id of the client the message is being sent to
        :return:
        """
        await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str):
        """
        send message to all active user
        :param message: message to be sent
        :return:
        """
        for connection in self.active_connections:
            await self.active_connections[connection].send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    logging out the user
    :param websocket: connection information
    :param client_id: id of the client who logs out
    :return:
    """
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")


# Dependency
# We need to have an independent database session/connection (SessionLocal) per request,
# use the same session through all the request and then close it after the request is finished.
# Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request,
# and then close it once the request is finished.
def get_db():
    """
    creating independent database session/connection (SessionLocal) per request
    :return: independent database session/connection (SessionLocal) per request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    set the active status to True for all active connections
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :param db: independent database session/connection (SessionLocal) per request
    :return: List of all users in database
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    for user in users:
        user.is_active = True if user.id in manager.active_connections else False
    return users


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    creating a new user
    :param user: new user to add to the database
    :param db: independent database session/connection (SessionLocal) per request
    :return: new user
    """
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    await manager.broadcast("status")
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=schemas.User)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    user login
    :param user: the user to be logged in
    :param db: independent database session/connection (SessionLocal) per request
    :return: user who has been logged in
    """
    user = crud.login_user(db, user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put('/users/status', response_model=schemas.User)
async def update_user_status(user: schemas.User, db: Session = Depends(get_db)):
    """
    user status update (is_active)
    :param user: the user to be updated
    :param db: independent database session/connection (SessionLocal) per request
    :return: updated user
    """
    db_user = crud.update_user_status(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id in manager.active_connections and not user.is_active:
        await manager.send_personal_message("offline", user.id)
    return user


@app.get('/user/kick', response_model=schemas.User)
async def kick_user(receiver_id: int, db: Session = Depends(get_db)):
    """
    kicking users off the server
    :param receiver_id: id of the user to be kicked from the server
    :param db: independent database session/connection (SessionLocal) per request
    :return: kicked user
    """
    db_user = crud.get_user(db, user_id=receiver_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id in manager.active_connections and db_user.is_active:
        await manager.send_personal_message("kick", db_user.id)
    return db_user


@app.put('/user/ban', response_model=schemas.User)
async def ban_user(user: schemas.UserBan, db: Session = Depends(get_db)):
    """
    banning users from the server
    :param user: the user to be banned from the server
    :param db: independent database session/connection (SessionLocal) per request
    :return: banned user
    """
    db_user = crud.update_user_status_ban(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id in manager.active_connections and db_user.is_active:
        await manager.send_personal_message("ban", db_user.id)
    return db_user


@app.get("/users/status/{status}")
def get_users_by_status(status: str, db: Session = Depends(get_db)):
    """
    search for all users with a given status
    :param status: the status of the is_active field
    :param db: independent database session/connection (SessionLocal) per request
    :return: all users with a given status
    """
    if status.lower() == "active":
        return crud.get_users_by_status(db, True)
    elif status.lower() == "inactive":
        return crud.get_users_by_status(db, False)
    else:
        raise HTTPException(status_code=404, detail="Status not found")


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    search for specified user with a given id
    :param user_id: id of the user to find
    :param db: independent database session/connection (SessionLocal) per request
    :return: searched user
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/message/", response_model=List[schemas.Message])
def read_all_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    give all messages contained in the database
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :param db: independent database session/connection (SessionLocal) per request
    :return: All messages form database
    """
    messages = crud.get_all_messages(db, skip=skip, limit=limit)
    return messages


@app.post("/message/{receiver_id}/", response_model=schemas.Message)
async def create_message_from_user(message: schemas.MessageCreate, receiver_id: int, db: Session = Depends(get_db)):
    """
    compose a new message
    :param message: the message that was sent to the user
    :param receiver_id: id of the user to whom the message was sent
    :param db: independent database session/connection (SessionLocal) per request
    :return: created message
    """
    if receiver_id == 0:
        await manager.broadcast("update_mess")
    elif receiver_id in manager.active_connections:
        await manager.send_personal_message("update_mess", receiver_id)
    if message.from_usr in manager.active_connections:
        await manager.send_personal_message("update_mess", message.from_usr)
    return crud.create_message(db=db, message=message, receiver_id=receiver_id)


@app.get("/message/{receiver_id}/{sender_id}/", response_model=List[schemas.Message])
def read_messages_to_user_from(receiver_id: int, sender_id: int, skip: int = 0, limit: int = 100,
                               db: Session = Depends(get_db)):
    """
    search for all messages from the user (sender_id) to user (receiver_id)
    :param receiver_id: id of the user to whom the message was sent
    :param sender_id: id of the user from whom the message was sent
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :param db: independent database session/connection (SessionLocal) per request
    :return: all messages from user (sender_id) to user (receiver_id)
    """
    messages = crud.get_messages_to_user_from(db, receiver_id=receiver_id, sender_id=sender_id, skip=skip,
                                              limit=limit)
    return messages


@app.get("/message/{receiver_id}/{sender_id}/{from_date}", response_model=List[schemas.Message])
def read_messages_to_user_from_date(receiver_id: int, sender_id: int, from_date: datetime, skip: int = 0,
                                    limit: int = 100, db: Session = Depends(get_db)):
    """
    search for all messages from the user (sender_id) to user (receiver_id) since given date
    :param receiver_id: id of the user to whom the message was sent
    :param sender_id: id of the user from whom the message was sent
    :param from_date: date from which to look for messages
    :param skip: number of first missed results
    :param limit: limit for searched queries
    :param db: independent database session/connection (SessionLocal) per request
    :return: all messages from user (sender_id) to user (receiver_id) since given date
    """
    if sender_id == 0:
        messages = crud.get_messages_to_general(db, from_date)
    else:
        messages = crud.get_messages_to_user_from_date(db, receiver_id=receiver_id, sender_id=sender_id, date=from_date,
                                                       skip=skip, limit=limit)
    return messages


@app.delete("/message/{message_id}")
def delete_message_by_id(message_id: int, db: Session = Depends(get_db)):
    """
    delete a message
    :param message_id: id of the message to delete
    :param db: independent database session/connection (SessionLocal) per request
    :return: confirmation that the operation was successful
    """
    if crud.delete_message_by_id(db, message_id):
        return status.HTTP_202_ACCEPTED
    return status.HTTP_204_NO_CONTENT
