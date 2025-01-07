# src/models/notification.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)

    # Relationship with User
    user = relationship("User", back_populates="notifications")

    def mark_as_read(self):
        self.is_read = True

    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, message={self.message}, is_read={self.is_read})>"
