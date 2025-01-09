# src/auth/two_factor_auth.py

import pyotp
import logging
from fastapi import HTTPException
from src.utils.config import config
from src.services.notification_service import NotificationService  # Assuming you have a notification service

logger = logging.getLogger(__name__)

def generate_otp_secret() -> str:
    """Generate a new OTP secret for 2FA."""
    return pyotp.random_base32()

def verify_otp(secret: str, otp: str) -> bool:
    """Verify the provided OTP against the secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def send_otp(secret: str, user_email: str) -> None:
    """Send OTP to the user's email or phone number."""
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    
    # Send OTP via email or SMS
    notification_service = NotificationService()
    notification_service.send_notification(user_email, f"Your OTP is: {otp}")
    
    logger.info(f"Sent OTP to {user_email}: {otp}")

def enable_two_factor_auth(user) -> None:
    """Enable 2FA for the user."""
    secret = generate_otp_secret()
    user.otp_secret = secret  # Assuming the User model has an otp_secret field
    # Save the user with the new OTP secret
    user.save()  # Implement the save method according to your ORM

    logger.info(f"2FA enabled for user {user.username}. Secret: {secret}")

def disable_two_factor_auth(user) -> None:
    """Disable 2FA for the user."""
    user.otp_secret = None  # Clear the OTP secret
    user.save()  # Implement the save method according to your ORM

    logger.info(f"2FA disabled for user {user.username}.")
