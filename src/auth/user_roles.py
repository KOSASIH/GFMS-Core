# src/auth/user_roles.py

from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    SUPER_ADMIN = "super_admin"  # New role for enhanced permissions

# Example of role-based access control
ROLE_PERMISSIONS = {
    UserRole.ADMIN: ["create_user", "delete_user", "view_all_users"],
    UserRole.USER: ["view_own_profile", "update_own_profile"],
    UserRole.MODERATOR: ["view_all_users", "update_user"],
    UserRole.SUPER_ADMIN: ["manage_roles", "view_all_data"],  # New permissions for super admin
}
