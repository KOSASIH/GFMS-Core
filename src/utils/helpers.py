# src/utils/helpers.py

from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format a datetime object as a string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def generate_unique_id() -> str:
    """Generate a unique identifier (UUID)."""
    import uuid
    return str(uuid.uuid4())
