# src/api/routes.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.auth.jwt import get_current_user
from src.services.user_service import UserService
from src.services.transaction_service import TransactionService

api_router = APIRouter()

# Example Pydantic models for request validation
class User(BaseModel):
    username: str
    email: str
    password: str

class Transaction(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

# User Registration Endpoint
@api_router.post("/register", response_model=User)
async def register_user(user: User):
    user_service = UserService()
    new_user = user_service.create_user(user.username, user.email, user.password)
    return new_user

# User Login Endpoint
@api_router.post("/login")
async def login_user(user: User):
    user_service = UserService()
    token = user_service.authenticate_user(user.username, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}

# Transaction Creation Endpoint
@api_router.post("/transactions", response_model=Transaction)
async def create_transaction(transaction: Transaction, current_user: str = Depends(get_current_user)):
    transaction_service = TransactionService()
    new_transaction = transaction_service.create_transaction(transaction.sender_id, transaction.receiver_id, transaction.amount)
    return new_transaction
