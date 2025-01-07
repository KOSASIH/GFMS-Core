# src/auth/password_reset.py

from fastapi import HTTPException
from src/services/user_service import UserService
from src.auth.jwt import create_access_token
import logging

logger = logging.getLogger(__name__)

def generate_password_reset_token(email: str):
    user_service = UserService()
    user = user_service.get_user_by_email(email)
    if not user:
        logger.error(f"Password reset attempt for non-existent user: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    
    token_data = {"sub": user.email}
    token = create_access_token(token_data, expires_delta=timedelta(hours=1))
    logger.info(f"Generated password reset token for user: {email}")
    return token

def reset_password(token: str, new_password: str):
    user_service = UserService()
    email = verify_token(token)["sub"]
    user_service.update_password(email, new_password)
    logger.info(f"Password reset successful for user: {email}")
