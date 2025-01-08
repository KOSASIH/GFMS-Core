# src/models/account.py

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func
from datetime import datetime
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")  # Default currency
    created_at = Column(String, default=datetime.utcnow)  # Store as ISO format string
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)  # Track updates

    # Relationship with User
    user = relationship("User ", back_populates="account")

    # Relationship with Transaction History
    transactions = relationship("Transaction", back_populates="account")

    def deposit(self, amount: float):
        if amount <= 0:
            logger.error("Deposit amount must be positive.")
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        logger.info(f"Deposited {amount} to account {self.id}. New balance: {self.balance}")

    def withdraw(self, amount: float):
        if amount <= 0:
            logger.error("Withdrawal amount must be positive.")
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            logger.error(f"Insufficient funds for withdrawal. Current balance: {self.balance}, Requested: {amount}")
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        logger.info(f"Withdrew {amount} from account {self.id}. New balance: {self.balance}")

    def transfer(self, target_account, amount: float):
        if amount <= 0:
            logger.error("Transfer amount must be positive.")
            raise ValueError("Transfer amount must be positive.")
        if amount > self.balance:
            logger.error(f"Insufficient funds for transfer. Current balance: {self.balance}, Requested: {amount}")
            raise ValueError("Insufficient funds.")
        if self.currency != target_account.currency:
            logger.error("Currency mismatch between accounts.")
            raise ValueError("Currency mismatch between accounts.")

        self.withdraw(amount)
        target_account.deposit(amount)
        logger.info(f"Transferred {amount} from account {self.id} to account {target_account.id}.")

    def get_transaction_history(self):
        # Assuming Transaction model has a foreign key to Account
        return self.transactions

    def __repr__(self):
        return f"<Account(id={self.id}, user_id={self.user_id}, balance={self.balance}, currency={self.currency})>"
