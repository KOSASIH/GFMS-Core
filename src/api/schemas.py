# src/api/schemas.py

from pydantic import BaseModel, EmailStr, condecimal
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

class TransactionBase(BaseModel):
    sender_id: int
    receiver_id: int
    amount: condecimal(gt=0)  # Amount must be greater than 0

class TransactionResponse(TransactionBase):
    id: int
    status: str  # e.g., "completed", "pending"
