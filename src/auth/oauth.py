# src/auth/oauth.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.services.user_service import UserService
from src.utils.oauth_client import OAuthClient  # Custom OAuth client utility

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_service = UserService()
    user = user_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

async def oauth_login(provider: str, code: str):
    oauth_client = OAuthClient(provider)
    user_info = oauth_client.get_user_info(code)
    user_service = UserService()
    user = user_service.get_or_create_user(user_info)
    return user
