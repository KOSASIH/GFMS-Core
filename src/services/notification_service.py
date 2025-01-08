# src/services/notification_service.py

import logging
from typing import List
from src.models.notification import Notification
from src.utils.email_client import EmailClient  # Assuming you have an email client utility
from src.utils.sms_client import SMSClient      # Assuming you have an SMS client utility
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        self.email_client = EmailClient()
        self.sms_client = SMSClient()

    def send_email_notification(self, user_email: str, subject: str, message: str):
        try:
            self.email_client.send_email(user_email, subject, message)
            logger.info(f"Email sent to {user_email} with subject: {subject}")
            self.log_notification(user_email, message)
        except Exception as e:
            logger.error(f"Failed to send email to {user_email}: {str(e)}")

    def send_sms_notification(self, user_phone: str, message: str):
        try:
            self.sms_client.send_sms(user_phone, message)
            logger.info(f"SMS sent to {user_phone}: {message}")
            self.log_notification(user_phone, message)
        except Exception as e:
            logger.error(f"Failed to send SMS to {user_phone}: {str(e)}")

    def log_notification(self, user_identifier: str, message: str):
        notification = Notification(user_id=user_identifier, message=message)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        logger.info(f"Notification logged: {notification}")

    def get_user_notifications(self, user_id: int) -> List[Notification]:
        return self.db.query(Notification).filter(Notification.user_id == user_id).all()
