# tests/integration/test_database.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base
from src.models.user import User
from src.models.account import Account

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    session.close()

def test_user_creation(test_db):
    user = User(username="dbuser", email="dbuser@example.com")
    user.set_password("securepassword")
    test_db.add(user)
    test_db.commit()
    
    assert user.id is not None
    assert test_db.query(User).filter_by(username="dbuser").first() is not None

def test_account_creation(test_db):
    user = User(username="accountuser", email="accountuser@example.com")
    user.set_password("securepassword")
    test_db.add(user)
    test_db.commit()
    
    account = Account(user_id=user.id, balance=500.0)
    test_db.add(account)
    test_db.commit()
    
    assert account.id is not None
    assert test_db.query(Account).filter_by(user_id=user.id).first() is not None
