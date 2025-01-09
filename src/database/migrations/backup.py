# src/database/migrations/backup.py

import os
import shutil
import logging
from datetime import datetime
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from src.database.db import DATABASE_URL

logger = logging.getLogger(__name__)

# Generate a key for encryption
def generate_key() -> bytes:
    """Generate a new encryption key."""
    return Fernet.generate_key()

# Save the key to a file
def save_key(key: bytes, key_file: str):
    """Save the encryption key to a file."""
    with open(key_file, "wb") as key_file_handle:
        key_file_handle.write(key)

# Load the key from a file
def load_key(key_file: str) -> bytes:
    """Load the encryption key from a file."""
    with open(key_file, "rb") as key_file_handle:
        return key_file_handle.read()

def encrypt_file(file_path: str, key: bytes):
    """Encrypt a file using the provided key."""
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(file_path: str, key: bytes):
    """Decrypt a file using the provided key."""
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def backup_database(backup_path: str, key_file: str):
    """Backup the database to the specified path with encryption."""
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    db_file = DATABASE_URL.split(":///")[-1]  # Extract the database file name
    backup_file = os.path.join(backup_path, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")

    try:
        # Create a backup of the database
        shutil.copy(db_file, backup_file)
        logger.info(f"Database backup created at: {backup_file}")

        # Generate and save the encryption key
        key = generate_key()
        save_key(key, key_file)

        # Encrypt the backup file
        encrypt_file(backup_file, key)
        logger.info(f"Backup file encrypted: {backup_file}")

    except Exception as e:
        logger.error(f"Error creating backup: {e}")

def restore_database(backup_file: str, key_file: str):
    """Restore the database from the specified backup file."""
    try:
        # Load the encryption key
        key = load_key(key_file)

        # Decrypt the backup file
        decrypt_file(backup_file, key)

        # Restore the database
        db_file = DATABASE_URL.split(":///")[-1]  # Extract the database file name
        shutil.copy(backup_file, db_file)
        logger.info(f"Database restored from: {backup_file}")

    except Exception as e:
        logger.error(f"Error restoring database: {e}")
