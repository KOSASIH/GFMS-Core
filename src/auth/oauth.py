# src/auth/oauth.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from httpx import AsyncClient
from src.utils.config import config
from src.models.user import User
from sqlalchemy.orm import Session
from src.database.db import get_db

router = APIRouter()

# OAuth2 configuration
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=config.OAUTH2_AUTHORIZATION_URL,
    tokenUrl=config.OAUTH2_TOKEN_URL,
)

@router.get("/login")
async def login():
    """Redirect to the OAuth provider for login."""
    return {"message": "Redirect to OAuth provider"}

@router.get("/callback")
async def callback(code: str, db: Session = Depends(get_db)):
    """Handle the callback from the OAuth provider."""
    async with AsyncClient() as client:
        # Exchange the authorization code for an access token
        token_response = await client.post(config.OAUTH2_TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.OAUTH2_REDIRECT_URI,
            "client_id": config.OAUTH2_CLIENT_ID,
            "client_secret": config.OAUTH2_CLIENT_SECRET,
        })

        token_data = token_response.json()
        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error_description"])

        access_token = token_data.get("access_token")

        # Use the access token to get user information
        user_info_response = await client.get(config.OAUTH2_USER_INFO_URL, headers={
            "Authorization": f"Bearer {access_token}"
        })

        user_info = user_info_response.json()
        if "error" in user_info:
            raise HTTPException(status_code=400, detail=user_info["error_description"])

        # Check if the user already exists in the database
        user = db.query(User).filter(User.email == user_info["email"]).first()
        if not user:
            # Create a new user if they don't exist
            user = User(
                username=user_info["name"],
                email=user_info["email"],
                # You may want to set a default password or handle it differently
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return {"access_token": access_token, "token_type": "bearer", "user": user}

@router.get("/logout")
async def logout():
    """Logout the user by invalidating the session."""
    return {"message": "User  logged out"}
