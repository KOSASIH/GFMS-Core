# src/auth/two_factor_auth.py

import pyotp
from fastapi import HTTPException
from src.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

def generate_2fa_secret(email: str):
    user_service = UserService()
    user = user_service.get_user_by_email(email)
    if not user:
        logger.error(f"2FA secret generation attempt for non-existent user: {email}")
        raise HTTPException(status_code=404, detail="User not found")
    
    secret = pyotp.random_base32()
    user_service.save_2fa_secret(email, secret)
    logger.info(f"Generated 2FA secret for user: {email}")
    return secret

def verify_2fa_token(email: str, token: str):
    user_service = UserService()
    secret = user_service.get_2fa_secret(email)
    if not secret:
        logger.error(f"2FA verification attempt for user without 2FA: {email}")
        raise HTTPException(status_code=400, detail="2FA not enabled for this user")
    
    totp = pyotp.TOTP(secret)
    if not totp.verify(token):
        logger.warning(f"Invalid 2FA token for user: {email}")
        raise HTTPException(status_code=400, detail="Invalid 2FA token")
    
    logger.info(f"2FA token verified successfully for user: {email}")
