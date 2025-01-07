# src/api/middleware.py

from fastapi import Request, Response
from starlette.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        logging.info(f"Request: {request.method} {request.url}")
        response: Response = await call_next(request)
        logging.info(f"Response: {response.status_code}")
        return response

# CORS Middleware
def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
