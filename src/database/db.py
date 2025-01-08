# src/database/db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import logging
import os

# Configure logging
logger = logging.getLogger(__name__)

# Database URL from environment variable or default to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # For SQLite

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session
db_session = scoped_session(SessionLocal)

# Base class for declarative models
Base = declarative_base()

def init_db():
    """Initialize the database and create tables."""
    logger.info("Initializing the database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")

def get_db():
    """Dependency to get the database session."""
    db = db_session()
    try:
        yield db
    finally:
        db.close()
