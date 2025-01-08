# src/models/notification.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)

class NotificationType(PyEnum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)  # Type of notification
    is_read = Column(Boolean, default=False)  # Status of the notification
    created_at = Column(String, default=datetime.utcnow)  # Timestamp of creation

    # Relationship with User
    user = relationship("User ", back_populates="notifications")

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        logger.info(f"Notification {self.id} marked as read.")

    def __repr__(self):
        return (f"<Notification(id={self.id}, user_id={self.user_id}, message={self.message}, "
                f"notification_type={self.notification_type}, is_read={self.is_read}, "
                f"created_at={self.created_at})>")

    @classmethod
    def create_notification(cls, session, user_id: int, message: str, notification_type: NotificationType):
        """Create a new notification."""
        notification = cls(user_id=user_id, message=message, notification_type=notification_type)
        session.add(notification)
        session.commit()
        session.refresh(notification)
        logger.info(f"Notification created: {notification}")
        return notification

    @classmethod
    def get_user_notifications(cls, session, user_id: int):
        """Retrieve all notifications for a specific user."""
        notifications = session.query(cls).filter(cls.user_id == user_id).all()
        logger.info(f"Retrieved {len(notifications)} notifications for user {user_id}.")
        return notifications

    @classmethod
    def get_unread_notifications(cls, session, user_id: int):
        """Retrieve all unread notifications for a specific user."""
        notifications = session.query(cls).filter(cls.user_id == user_id, cls.is_read == False).all()
        logger.info(f"Retrieved {len(notifications)} unread notifications for user {user_id}.")
        return notifications
