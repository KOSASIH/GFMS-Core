# src/utils/encryption.py

from cryptography.fernet import Fernet
import base64
import os

def generate_key() -> bytes:
    """Generate a new encryption key."""
    return base64.urlsafe_b64encode(os.urandom(32))

def encrypt_data(data: str, key: bytes) -> str:
    """Encrypt data using the provided key."""
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """Decrypt data using the provided key."""
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data.encode())
    return decrypted_data```python
.decode()
