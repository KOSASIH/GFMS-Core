# src/utils/security.py

import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from src.utils.config import config
from src.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str = Security(oauth2_scheme)):
    payload = verify_token(token)
    user = User.get_user_by_id(payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=401, detail="User  not found")
    return user
