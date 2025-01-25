import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="GFMS-Core API", version="1.0.0")

# OAuth2 scheme for security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample data models
class User(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None

class Transaction(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str

# Sample in-memory data storage (replace with a database in production)
users_db = {}
transactions_db = {}

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Here you would normally validate the token and retrieve the user
    user = users_db.get(1)  # Simulating user retrieval
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return user

# API Endpoints
@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(1)  # Simulating user retrieval
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/", response_model=List[User], tags=["Users"])
async def get_users(current_user: User = Depends(get_current_user)):
    """Retrieve a list of users."""
    return list(users_db.values())

@app.get("/transactions/", response_model=List[Transaction], tags=["Transactions"])
async def get_transactions(current_user: User = Depends(get_current_user)):
    """Retrieve a list of transactions for the current user."""
    return list(transactions_db.values())

@app.post("/users/", response_model=User, tags=["Users"])
async def create_user(user: User):
    """Create a new user."""
    if user.id in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user.password = get_password_hash(user.password)  # Hash the password
    users_db[user.id] = user
    return user

@app.post("/transactions/", response_model=Transaction, tags=["Transactions"])
async def create_transaction(transaction: Transaction, current_user: User = Depends(get_current_user)):
    """Create a new transaction for the current user."""
    transactions_db[transaction.id] = transaction
    return transaction

# Custom OpenAPI schema generation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="GFMS-Core API",
        version="1.0.0",
        description="This is the API documentation for the GFMS-Core project.",
        routes=app.routes,
    )
    # Add custom metadata
    openapi_schema["info"]["termsOfService"] = "http://example.com/terms/"
    openapi_schema["info"]["contact"] = {
        "name": "Support",
        "url": "http://example.com/support",
        "email": "support@example.com",
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
