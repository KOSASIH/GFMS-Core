# src/models/settings.py

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)

class SettingType:
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)  # Unique key for the setting
    value = Column(String, nullable=False)  # Store value as string for flexibility
    type = Column(String, nullable=False)  # Type of the setting (string, integer, float, boolean)

    def __repr__(self):
        return f"<Settings(id={self.id}, key={self.key}, value={self.value}, type={self.type})>"

    @classmethod
    def get_setting(cls, session, key: str):
        """Retrieve a setting by its key."""
        setting = session.query(cls).filter(cls.key == key).first()
        if setting:
            logger.info(f"Retrieved setting: {setting}")
            return setting
        else:
            logger.warning(f"Setting not found for key: {key}")
            return None

    @classmethod
    def update_setting(cls, session, key: str, value: str):
        """Update the value of a setting."""
        setting = session.query(cls).filter(cls.key == key).first()
        if setting:
            setting.value = value
            session.commit()
            logger.info(f"Updated setting: {setting}")
        else:
            logger.warning(f"Setting not found for key: {key}")

    @classmethod
    def create_setting(cls, session, key: str, value: str, setting_type: str):
        """Create a new setting."""
        if session.query(cls).filter(cls.key == key).first():
            logger.error(f"Setting already exists for key: {key}")
            raise ValueError("Setting with this key already exists.")
        
        setting = cls(key=key, value=value, type=setting_type)
        session.add(setting)
        session.commit()
        session.refresh(setting)
        logger.info(f"Created setting: {setting}")
        return setting
