# tests/unit/test_notification.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.db import Base
from src.models.notification import Notification
from src.services.notification_service import NotificationService

@pytest.fixture(scope='module')
def test_db():
    # Set up the database for testing
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    session.close()

def test_send_notification(test_db):
    notification_service = NotificationService(test_db)
    notification = notification_service.send_notification("user1@example.com", "Test Notification", "This is a test message.")
    
    assert notification.recipient == "user1@example.com"
    assert notification.message == "This is a test message."
    assert notification.status == "sent"

def test_notification_history(test_db):
    notification_service = NotificationService(test_db)
    notification_service.send_notification("user2@example.com", "Another Test", "This is another test message.")
    
    history = notification_service.get_notification_history("user2@example.com")
    
    assert len(history) == 1
    assert history[0].message == "This is another test message."
