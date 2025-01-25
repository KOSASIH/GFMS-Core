import time
from fastapi import Request, HTTPException
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int, time_window: int):
        super().__init__(app)
        self.rate_limit = rate_limit  # Maximum number of requests allowed
        self.time_window = time_window  # Time window in seconds
        self.requests = defaultdict(list)  # Store timestamps of requests

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host  # Get the client's IP address
        current_time = time.time()

        # Clean up old requests
        self.requests[client_ip] = [
            timestamp for timestamp in self.requests[client_ip]
            if current_time - timestamp < self.time_window
        ]

        # Check if the rate limit has been exceeded
        if len(self.requests[client_ip]) >= self.rate_limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

        # Record the current request
        self.requests[client_ip].append(current_time)

        # Process the request
        response = await call_next(request)
        return response

# Example usage in a FastAPI application
if __name__ == "__main__":
    from fastapi import FastAPI

    app = FastAPI(middleware=[
        Middleware(RateLimiterMiddleware, rate_limit=5, time_window=60)  # 5 requests per minute
    ])

    @app.get("/example")
    async def example_endpoint():
        return {"message": "This is an example endpoint."}

    # To run the application, use:
    # uvicorn rate_limiter:app --host 0.0.0.0 --port 8000 --reload
