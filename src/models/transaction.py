# src/models/transaction.py

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # e.g., "pending", "completed", "failed"
    created_at = Column(String, default=datetime.utcnow)  # Store as ISO format string

    # Relationships
    sender = relationship("User", back_populates="transactions_sent", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="transactions_received", foreign_keys=[receiver_id])

    def __repr__(self):
        return f"<Transaction(id={self.id}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, amount={self.amount}, status={self.status})>"
