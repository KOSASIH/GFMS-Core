# src/utils/validators.py

import re

def validate_email(email: str) -> bool:
    """Validate an email address."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_username(username: str) -> bool:
    """Validate a username."""
    return len(username) >= 3 and len(username) <= 30

def validate_password(password: str) -> bool:
    """Validate a password."""
    return len(password) >= 8

def validate_positive_number(value: float) -> bool:
    """Validate that a number is positive."""
    return value > 0
