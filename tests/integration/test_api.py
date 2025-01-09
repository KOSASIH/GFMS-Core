# tests/integration/test_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base, get_db
from src.main import app
from src.models.user import User
from src.models.account import Account

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create test data
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    session.add(user)
    session.commit()
    
    account = Account(user_id=user.id, balance=1000.0)
    session.add(account)
    session.commit()
    
    yield session
    session.close()

@pytest.fixture(scope='module')
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c

def test_create_user(client):
    response = client.post("/api/users/", json={"username": "newuser", "email": "new@example.com", "password": "newpassword"})
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_authenticate_user(client):
    response = client.post("/api/token", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_transaction(client):
    response = client.post("/api/transactions/", json={"sender_id": 1, "receiver_id": 2, "amount": 100.0})
    assert response.status_code == 200
    assert response.json()["amount"] == 100.0
