# tests/unit/test_transaction.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base
from src.models.user import User
from src.models.transaction import Transaction
from src.models.account import Account
from src.services.transaction_service import TransactionService

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create test data
    user1 = User(username="user1", email="user1@example.com")
    user2 = User(username="user2", email="user2@example.com")
    account1 = Account(user_id=1, balance=1000.0)
    account2 = Account(user_id=2, balance=500.0)
    
    session.add(user1)
    session.add(user2)
    session.add(account1)
    session.add(account2)
    session.commit()
    
    yield session
    session.close()

def test_create_transaction(test_db):
    transaction_service = TransactionService(test_db)
    transaction = transaction_service.create_transaction(sender_id=1, receiver_id=2, amount=100.0)
    
    assert transaction.amount == 100.0
    assert transaction.status == "completed"

def test_insufficient_funds(test_db):
    transaction_service = TransactionService(test_db)
    
    with pytest.raises(ValueError):
        transaction_service.create_transaction(sender_id=1, receiver_id=2, amount=2000.0)
