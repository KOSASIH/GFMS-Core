# src/api.py

from fastapi import APIRouter, Depends
from src.utils.security import create_access_token, get_current_user
from src.models.user import User
from src.services.user_service import UserService
from sqlalchemy.orm import Session
from src.database.db import get_db

app = APIRouter()

@app.post("/token")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.authenticate_user(username, password)
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
