# src/database/migrations/seed_data.py

from sqlalchemy.orm import Session
from src.models.user import User
from src.models.account import Account
import logging

logger = logging.getLogger(__name__)

def seed_users(db: Session):
    """Seed initial users into the database."""
    users = [
        User(username="admin", email="admin@example.com", is_verified=True),
        User(username="user1", email="user1@example.com", is_verified=True),
        User(username="user2", email="user2@example.com", is_verified=False),
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    logger.info("Seeded initial users.")

def seed_accounts(db: Session):
    """Seed initial accounts into the database."""
    accounts = [
        Account(user_id=1, balance=1000.0, currency="USD"),
        Account(user_id=2, balance=500.0, currency="USD"),
        Account(user_id=3, balance=0.0, currency="USD"),
    ]
    
   for account in accounts:
        db.add(account)
    
    db.commit()
    logger.info("Seeded initial accounts.")

def seed_data(db: Session):
    """Seed all initial data."""
    seed_users(db)
    seed_accounts(db)
    logger.info("All initial data seeded successfully.")
