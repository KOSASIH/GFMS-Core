# swagger.py
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(
        title="GFMS API",
        version="1.0.0",
        description="API documentation for the GFMS application.",
        routes=app.routes,
    )

@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Swagger UI")

# Example of a sample endpoint
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return {"item_id": item_id, "name": "Sample Item"}

# To run the application, use the command:
# uvicorn swagger:app --reload
