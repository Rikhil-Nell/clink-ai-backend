import redis.asyncio as redis
import json
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.app.core.config import settings
from backend.app.schemas.token import AuthData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_current_auth_data(token: str = Depends(oauth2_scheme)) -> AuthData:
    """
    Validates token against Redis cache and returns the associated
    user_id and loyalty_program_id.
    """
    # Assumes you store a JSON string like: '{"user_id": 123, "loyalty_program_id": 456}'
    auth_data_str = await redis_client.get(f"auth_token:{token}")
    
    if not auth_data_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
        
    try:
        # Parse the JSON string from Redis into our Pydantic model
        data = json.loads(auth_data_str)
        return AuthData(**data)
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not parse authentication data.",
        )