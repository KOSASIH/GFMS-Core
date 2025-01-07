# src/auth/permissions.py

from fastapi import Depends, HTTPException
from src.auth.user_roles import UserRole, ROLE_PERMISSIONS
from src.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

def check_permissions(required_permission: str):
    def decorator(user: UserRole = Depends(get_current_user)):
        if required_permission not in ROLE_PERMISSIONS.get(user.role, []):
            logger.warning(f"Permission denied for user {user.username} on {required_permission}")
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return decorator
