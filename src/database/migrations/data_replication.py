import os
import time
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core Data Replication API", version="1.0.0")

# In-memory storage for data (replace with actual database connections in production)
data_store = {
    "primary": {"data": "Primary data"},
    "replica": {"data": None},
}

# Data model for replication request
class ReplicationRequest(BaseModel):
    source: str
    target: str

# Endpoint to initiate data replication
@app.post("/replicate", response_model=dict, tags=["Data Replication"])
async def replicate_data(request: ReplicationRequest):
    """Initiate data replication from source to target."""
    source = request.source
    target = request.target

    if source not in data_store or target not in data_store:
        raise HTTPException(status_code=400, detail="Invalid source or target specified")

    try:
        # Simulate data replication process
        logger.info(f"Starting replication from {source} to {target}...")
        time.sleep(2)  # Simulate time taken for replication
        data_store[target]["data"] = data_store[source]["data"]
        logger.info(f"Replication from {source} to {target} completed successfully.")
        return {"message": "Data replicated successfully", "target_data": data_store[target]["data"]}
    except Exception as e:
        logger.error(f"Error during replication: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to replicate data")

# Endpoint to check the status of the data replication
@app.get("/replication_status", response_model=Dict[str, str], tags=["Data Replication"])
async def replication_status():
    """Check the status of the data replication."""
    return {
        "primary_data": data_store["primary"]["data"],
        "replica_data": data_store["replica"]["data"],
        "status": "Replication successful" if data_store["replica"]["data"] else "Replication not yet performed"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
