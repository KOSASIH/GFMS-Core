# tests/e2e/test_transaction_flows.py

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
    
    # Create test users and accounts
    user1 = User(username="user1", email="user1@example.com")
    user1.set_password("password123")
    session.add(user1)
    
    user2 = User(username="user2", email="user2@example.com")
    user2.set_password("password123")
    session.add(user2)
    
    session.commit()
    
    account1 = Account(user_id=user1.id, balance=1000.0)
    account2 = Account(user_id=user2.id, balance=500.0)
    session.add(account1)
    session.add(account2)
    session.commit()
    
    yield session
    session.close()

@pytest.fixture(scope='module')
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c

def test_create_transaction(client):
    # Log in user1
    login_response = client.post("/api/token", data={"username": "user1", "password": "password123"})
    token = login_response.json()["access_token"]
    
    # Create a transaction
    response = client.post("/api/transactions/", json={"sender_id": 1, "receiver_id": 2, "amount": 100.0}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["amount"] == 100.0

def test_view_transaction_history(client):
    # Log in user1
    login_response```python
    = client.post("/api/token", data={"username": "user1", "password": "password123"})
    token = login_response.json()["access_token"]
    
    # View transaction history
    response = client.get("/api/transactions/history", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure the response is a list
    assert len(response.json()) > 0  # Ensure there is at least one transaction

def test_transaction_failure(client):
    # Log in user1
    login_response = client.post("/api/token", data={"username": "user1", "password": "password123"})
    token = login_response.json()["access_token"]
    
    # Attempt to create a transaction with insufficient funds
    response = client.post("/api/transactions/", json={"sender_id": 1, "receiver_id": 2, "amount": 2000.0}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400  # Expect a failure due to insufficient funds
    assert "Insufficient funds" in response.json()["detail"]
