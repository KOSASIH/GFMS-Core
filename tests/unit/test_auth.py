# tests/unit/test_auth.py

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
    
    # Create test user
    user = User(username="authuser", email="auth@example.com")
    user.set_password("securepassword")
    session.add(user)
    session.commit()
    
    yield session
    session.close()

def test_authenticate_user(test_db):
    user_service = UserService(test_db)
    token = user_service.authenticate_user("authuser", "securepassword")
    
    assert token is not None

def test_invalid_authentication(test_db):
    user_service = UserService(test_db)
    
    with pytest.raises(ValueError):
        user_service.authenticate_user("authuser", "wrongpassword")
