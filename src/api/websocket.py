import json
import logging
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a router for WebSocket routes
router = APIRouter()

# Store connected WebSocket clients
clients: List[WebSocket] = []

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    clients.append(websocket)
    logger.info(f"Client connected: {websocket.client}")

    try:
        while True:
            # Wait for a message from the client
            data = await websocket.receive_text()
            logger.info(f"Received message from {websocket.client}: {data}")
            await broadcast(data)
    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {websocket.client}")
        clients.remove(websocket)

async def broadcast(message: str):
    """Broadcast a message to all connected clients."""
    for client in clients:
        try:
            await client.send_text(message)
            logger.info(f"Sent message to {client.client}: {message}")
        except Exception as e:
            logger.error(f"Error sending message to {client.client}: {e}")

def send_update(data: dict):
    """Send an update to all connected clients."""
    message = json.dumps(data)
    logger.info(f"Broadcasting update: {message}")
    # Call the broadcast function in an event loop
    import asyncio
    asyncio.run(broadcast(message))

# Example usage
if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()

    # Include the WebSocket router
    app.include_router(router)

    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)
