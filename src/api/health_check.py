# health_check.py
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

router = APIRouter()

@router.get("/health", status_code=HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to monitor the status of the application.
    Returns a 200 OK response if the application is healthy.
    """
    try:
        # Here you can add checks for database connectivity, external services, etc.
        # For example, checking if the database is reachable:
        # db_status = check_database_connection()
        # if not db_status:
        #     raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail="Database is down")

        return {"status": "healthy"}
    except Exception as e:
        # Log the exception (optional)
        # logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail="Service is unavailable")

# To include this router in your main application, you would do something like:
# from fastapi import FastAPI
# from .health_check import router as health_check_router

# app = FastAPI()
# app.include_router(health_check_router)
