# src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import app as api_app
from src.database.db import init_db
from src.utils.logger import setup_logger
from src.utils.config import config
import logging

# Set up logging
logger = setup_logger('GFMS', 'gfms.log')

# Initialize FastAPI app
app = FastAPI(title="Global Financial Management System API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the database
init_db()

# Include the API router
app.mount("/api", api_app)

@app.get("/")
async def root():
    return {"message": "Welcome to the Global Financial Management System API"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the application...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
