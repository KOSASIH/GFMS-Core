# src/main.py

from fastapi import FastAPI
from src.api import app as api_app
from src.api.middleware import add_cors_middleware, LoggingMiddleware

app = FastAPI(title="Global Financial Management System")

# Add CORS and logging middleware
add_cors_middleware(app)
app.add_middleware(LoggingMiddleware)

# Include the API application
app.mount("/api", api_app)
