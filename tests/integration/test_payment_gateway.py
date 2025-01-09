# tests/integration/test_payment_gateway.py

import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base
from src.models.transaction import Transaction
from src.services.payment_gateway_service import PaymentGatewayService

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    session.close()

def test_process_payment(test_db):
    payment_service = PaymentGatewayService(test_db)
    
    # Mock the payment gateway response
    with patch('src.utils.payment_gateway .mock_payment_gateway') as mock_gateway:
        mock_gateway.return_value = {"status": "success", "transaction_id": "12345"}
        
        transaction = payment_service.process_payment(sender_id=1, receiver_id=2, amount=100.0)
        
        assert transaction.status == "completed"
        assert transaction.transaction_id == "12345"

def test_payment_failure(test_db):
    payment_service = PaymentGatewayService(test_db)
    
    # Mock the payment gateway response for failure
    with patch('src.utils.payment_gateway.mock_payment_gateway') as mock_gateway:
        mock_gateway.return_value = {"status": "failure", "error": "Insufficient funds"}
        
        with pytest.raises(ValueError) as excinfo:
            payment_service.process_payment(sender_id=1, receiver_id=2, amount=2000.0)
        
        assert "Insufficient funds" in str(excinfo.value)
