# src/services/user_service.py

from sqlalchemy.orm import Session
from src.models.user import User
from src.auth.jwt import create_access_token
from src.utils.exceptions import UserNotFoundException, UserAlreadyExistsException
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password: str) -> User:
        existing_user = self.db.query(User).filter((User .username == username) | (User .email == email)).first()
        if existing_user:
            logger.error(f"User  creation failed: User already exists (username={username}, email={email})")
            raise UserAlreadyExistsException("User  with this username or email already exists.")

        user = User(username=username, email=email)
        user.set_password(password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(f"User  created successfully: {user}")
        return user

    def authenticate_user(self, username: str, password: str) -> str:
        user = self.db.query(User).filter(User.username == username).first()
        if not user or not user.verify_password(password):
            logger.error("Authentication failed: Invalid username or password.")
            raise UserNotFoundException("Invalid username or password.")

        token = create_access_token(data={"sub": user.username})
        logger.info(f"User  authenticated successfully: {user.username}")
        return token

    def get_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            logger.error(f"User  retrieval failed: User not found (email={email})")
            raise UserNotFoundException("User  not found.")
        return user

    def get_user_from_token(self, token: str) -> User:
        payload = verify_token(token)
        user = self.db.query(User).filter(User.username == payload["sub"]).first()
        if not user:
            logger.error("User  retrieval failed: User not found from token.")
            raise UserNotFoundException("User  not found.")
        return user
