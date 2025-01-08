# src/services/analytics_service.py

from sqlalchemy.orm import Session
from src.models.transaction import Transaction
from src.models.user import User
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_activity(self, user_id: int):
        transactions = self.db.query(Transaction).filter((Transaction.sender_id == user_id) | (Transaction.receiver_id == user_id)).all()
        logger.info(f"Retrieved activity for user {user_id}: {len(transactions)} transactions found.")
        return transactions

    def get_transaction_summary(self):
        total_transactions = self.db.query(Transaction).count()
        total_amount = self.db.query(Transaction).with_entities(func.sum(Transaction.amount)).scalar() or 0
        logger.info(f"Transaction summary: {total_transactions} transactions totaling {total_amount}.")
        return {
            "total_transactions": total_transactions,
            "total_amount": total_amount
        }

    def get_user_statistics(self):
        users = self.db.query(User).all()
        user_stats = {
            "total_users": len(users),
            "active_users": len([user for user in users if user.is_active]),
            "verified_users": len([user for user in users if user.is_verified]),
        }
        logger.info(f"User  statistics: {user_stats}")
        return user_stats
