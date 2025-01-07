# src/api/versioning.py

from fastapi import APIRouter, Depends

api_router_v1 = APIRouter()

# Example of a versioned endpoint
@api_router_v1.get("/status")
async def get_status():
    return {"status": "API is running", "version": "v1"}

# You can create additional versions as needed
