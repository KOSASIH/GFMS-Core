import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core Monitoring API", version="1.0.0")

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total request count", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["method", "endpoint"])

# Middleware for monitoring requests
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    # Start timer
    with REQUEST_LATENCY.labels(method, endpoint).time():
        response = await call_next(request)

    # Increment request count
    REQUEST_COUNT.labels(method, endpoint).inc()
    return response

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

# Example endpoint to demonstrate monitoring
@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={"status": "healthy"})

# Example endpoint to simulate an error
@app.get("/error", tags=["Monitoring"])
async def error_endpoint():
    """Simulate an error for monitoring."""
    logger.error("Simulated error occurred.")
    raise HTTPException(status_code=500, detail="Simulated error")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
