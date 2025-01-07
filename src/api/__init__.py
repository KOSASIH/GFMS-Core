# src/api/__init__.py

from fastapi import FastAPI
from .routes import api_router

app = FastAPI(title="Global Financial Management System API")

# Include the API router
app.include_router(api_router, prefix="/api/v1", tags=["API"])
