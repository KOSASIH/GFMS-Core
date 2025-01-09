# tests/e2e/test_user_flows.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base, get_db
from src.main import app
from src.models.user import User

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    session.close()

@pytest.fixture(scope='module')
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as c:
        yield c

def test_user_registration(client):
    response = client.post("/api/users/", json={"username": "newuser", "email": "new@example.com", "password": "newpassword"})
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_user_login(client):
    response = client.post("/api/token", data={"username": "newuser", "password": "newpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_user_profile(client):
    # Assuming the user is logged in and we have a valid token
    login_response = client.post("/api/token", data={"username": "newuser", "password": "newpassword"})
    token = login_response.json()["access_token"]
    
    response = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
