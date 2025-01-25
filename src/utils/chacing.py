import os
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core Caching API", version="1.0.0")

# Initialize Redis client
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Data model for caching
class CacheItem(BaseModel):
    key: str
    value: str
    expiration: int  # Expiration time in seconds

# Endpoint to set a cache item
@app.post("/cache/set", response_model=dict, tags=["Caching"])
async def set_cache_item(item: CacheItem):
    """Set a cache item with an expiration time."""
    try:
        redis_client.set(item.key, item.value, ex=item.expiration)
        logger.info(f"Cache item set: {item.key} = {item.value} (expires in {item.expiration} seconds)")
        return {"message": "Cache item set successfully"}
    except Exception as e:
        logger.error(f"Error setting cache item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to set cache item")

# Endpoint to get a cache item
@app.get("/cache/get/{key}", response_model=dict, tags=["Caching"])
async def get_cache_item(key: str):
    """Get a cache item by key."""
    try:
        value = redis_client.get(key)
        if value is None:
            raise HTTPException(status_code=404, detail="Cache item not found")
        logger.info(f"Cache item retrieved: {key} = {value}")
        return {"key": key, "value": value}
    except Exception as e:
        logger.error(f"Error retrieving cache item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve cache item")

# Endpoint to delete a cache item
@app.delete("/cache/delete/{key}", response_model=dict, tags=["Caching"])
async def delete_cache_item(key: str):
    """Delete a cache item by key."""
    try:
        result = redis_client.delete(key)
        if result == 0:
            raise HTTPException(status_code=404, detail="Cache item not found")
        logger.info(f"Cache item deleted: {key}")
        return {"message": "Cache item deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting cache item: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete cache item")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
