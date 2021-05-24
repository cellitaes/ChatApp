from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from server.database import SessionLocal, engine

from server import schemas, crud, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChatUp")


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict() = dict()

    async def connect(self, websocket: WebSocket, client_id):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        await manager.broadcast(f"status")

    async def disconnect(self, client_id):
        self.active_connections.pop(client_id)
        await manager.broadcast(f"status")

    async def send_personal_message(self, message: str, client_id):
        await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await self.active_connections[connection].send_text(message)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    # zakomentować, żeby była aktywność z bazy danych, bez websocket
    for usr in users:
        if usr.id in manager.active_connections:
            usr.is_active = True
        else:
            usr.is_active = False
    # tu koniec
    return users


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already registered")
    await manager.broadcast("status")
    return crud.create_user(db=db, user=user)


@app.post("/users/login", response_model=schemas.User)
def login_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.login_user(db, user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put('/users/status', response_model=schemas.User)
async def update_user_status(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.update_user_status(db, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await manager.broadcast("status")
    if user.id in manager.active_connections:
        if not user.is_active:
            await manager.send_personal_message("offline", user.id)
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
async def create_message_from_user(message: schemas.MessageCreate, receiver_id: int, db: Session = Depends(get_db)):
    if receiver_id in manager.active_connections:
        await manager.send_personal_message("new_message", receiver_id)
    if message.from_usr in manager.active_connections:
        await manager.send_personal_message("new_message", message.from_usr)
    return crud.create_message(db=db, message=message, receiver_id=receiver_id)


@app.get("/message/{receiver_id}/{sender_id}/", response_model=List[schemas.Message])
def read_messages_to_user_from(receiver_id: int, sender_id: int, skip: int = 0, limit: int = 100,
                               db: Session = Depends(get_db)):
    messages = crud.get_messages_to_user_from(db, receiver_id=receiver_id, sender_id=sender_id, skip=skip, limit=limit)
    return messages


@app.get("/message/{receiver_id}/{sender_id}/{from_date}", response_model=List[schemas.Message])
def read_messages_to_user_from_date(receiver_id: int, sender_id: int, from_date: datetime, skip: int = 0,
                                    limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages_to_user_from_date(db, receiver_id=receiver_id, sender_id=sender_id, date=from_date,
                                                   skip=skip, limit=limit)
    return messages


@app.post("/message/{receiver_id}/{sender_id}/latest", response_model=datetime)
def read_messages_to_user_from_latest(receiver_id: int, sender_id: int, db: Session = Depends(get_db)):
    date = crud.get_messages_to_user_from_latest(db=db, receiver_id=receiver_id, sender_id=sender_id)
    return date


@app.put("/message/{receiver_id}/read")
async def update_message_status(receiver_id: int, messages_ids: list, db: Session = Depends(get_db)):
    message = crud.update_message_status(db, receiver_id, messages_ids)
    if message is None:
        raise HTTPException(status_code=404, detail="User or messages not found")
    await manager.send_personal_message("read", receiver_id)
    await manager.broadcast("read")
    return status.HTTP_200_OK


@app.post("/message/{receiver_id}/{sender_id}/unread")
def unread_messages_to_user_from(receiver_id: int, sender_id: int, db: Session = Depends(get_db)):
    return crud.unread_messages_to_user_from(db, receiver_id=receiver_id, sender_id=sender_id)


@app.delete("/message/{message_id}")
def delete_message_by_id(message_id: int, db: Session = Depends(get_db)):
    if crud.delete_message_by_id(db, message_id):
        return status.HTTP_202_ACCEPTED
    return status.HTTP_204_NO_CONTENT
