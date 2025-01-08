# src/services/transaction_service.py

from sqlalchemy.orm import Session
from src.models.transaction import Transaction
from src.models.user import User
from src.models.account import Account
from src.utils.exceptions import InsufficientFundsException, TransactionError
import logging

logger = logging.getLogger(__name__)

class TransactionService:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, sender_id: int, receiver_id: int, amount: float) -> Transaction:
        # Validate transaction
        sender = self.db.query(User).filter(User.id == sender_id).first()
        receiver = self.db.query(User).filter(User.id == receiver_id).first()
        sender_account = self.db.query(Account).filter(Account.user_id == sender_id).first()
        
        if not sender or not receiver:
            logger.error(f"Transaction failed: User not found (sender_id={sender_id}, receiver_id={receiver_id})")
            raise TransactionError("Sender or receiver not found.")
        
        if amount <= 0:
            logger.error("Transaction failed: Amount must be greater than zero.")
            raise TransactionError("Transaction amount must be greater than zero.")
        
        if sender_account.balance < amount:
            logger.error(f"Transaction failed: Insufficient funds for user {sender.username}.")
            raise InsufficientFundsException("Insufficient funds for transaction.")

        # Create transaction
        transaction = Transaction(sender_id=sender_id, receiver_id=receiver_id, amount=amount)
        sender_account.withdraw(amount)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)

        logger.info(f"Transaction successful: {transaction}")
        return transaction
