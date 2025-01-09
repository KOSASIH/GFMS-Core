# tests/unit/test_user.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base
from src.models.user import User
from src.services.user_service import UserService

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(test_db):
    user_service = UserService(test_db)
    user = user_service.create_user("testuser", "test@example.com", "password123")
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.verify_password("password123") is True

def test_user_exists(test_db):
    user_service = UserService(test_db)
    user_service.create_user("existinguser", "existing@example.com", "password123")
    
    with pytest.raises(ValueError):
        user_service.create_user("existinguser", "new@example.com", "password123")
