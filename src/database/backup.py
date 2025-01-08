# src/database/backup.py

import os
import shutil
import logging
from sqlalchemy.orm import Session
from src.database.db import DATABASE_URL

logger = logging.getLogger(__name__)

def backup_database(backup_path: str):
    """Backup the database to the specified path."""
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    
    db_file = DATABASE_URL.split(":///")[-1]  # Extract the database file name
    backup_file = os.path.join(backup_path, f"backup_{db_file}")
    
    try:
        shutil.copy(db_file, backup_file)
        logger.info(f"Database backup created at: {backup_file}")
    except Exception as e:
        logger.error(f"Error creating backup: {e}")

def restore_database(backup_file: str):
    """Restore the database from the specified backup file."""
    db_file = DATABASE_URL.split(":///")[-1]  # Extract the database file name
    
    try:
        shutil.copy(backup_file, db_file)
        logger.info(f"Database restored from: {backup_file}")
    except Exception as e:
        logger.error(f"Error restoring database: {e}")
