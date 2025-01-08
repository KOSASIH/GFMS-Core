# src/models/audit_log.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)  # Description of the action performed
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp of the action
    ip_address = Column(String, nullable=True)  # IP address of the user
    details = Column(String, nullable=True)  # Additional details about the action

    # Relationship with User
    user = relationship("User ", back_populates="audit_logs")

    def __repr__(self):
        return (f"<AuditLog(id={self.id}, user_id={self.user_id}, action={self.action}, "
                f"timestamp={self.timestamp}, ip_address={self.ip_address}, details={self.details})>")

    @classmethod
    def log_action(cls, session, user_id: int, action: str, ip_address: str = None, details: str = None):
        """Log an action performed by a user."""
        log_entry = cls(user_id=user_id, action=action, ip_address=ip_address, details=details)
        session.add(log_entry)
        session.commit()
        session.refresh(log_entry)
        logger.info(f"Action logged: {log_entry}")

    @classmethod
    def get_logs_by_user(cls, session, user_id: int):
        """Retrieve all audit logs for a specific user."""
        logs = session.query(cls).filter(cls.user_id == user_id).all()
        logger.info(f"Retrieved {len(logs)} logs for user {user_id}.")
        return logs

    @classmethod
    def get_recent_logs(cls, session, limit: int = 100):
        """Retrieve the most recent audit logs."""
        logs = session.query(cls).order_by(cls.timestamp.desc()).limit(limit).all()
        logger.info(f"Retrieved {len(logs)} recent logs.")
        return logs
