# src/api/throttling.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time

class ThrottlingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int, period: int):
        super().__init__(app)
        self.limit = limit  # Maximum requests allowed
        self.period = period  # Time period in seconds
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean up old requests
        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if current_time - timestamp < self.period]

        if len(self.requests[client_ip]) >= self.limit:
            raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")

        # Record the request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response
