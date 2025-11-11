import redis.asyncio as redis
import asyncpg
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
from app.schemas.core.auth import AuthData
from app.db.database import get_db_pool
from app.crud.business_user_crud import get_loyalty_program_id_by_business_user_id

auth_scheme = APIKeyHeader(name="Authorization")
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_current_auth_data(token: str = Depends(auth_scheme),pool: asyncpg.Pool = Depends(get_db_pool)) -> AuthData:
    """
    Validates token against Redis cache and returns the associated
    user_id and loyalty_program_id.
    """
    business_user_id = await redis_client.get(f"business_user_token:{token}")
    if not business_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    loyalty_program_id = await get_loyalty_program_id_by_business_user_id(pool, int(business_user_id))
    if not loyalty_program_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No loyalty_program_id found for business user.",
        )

    return AuthData(user_id=int(business_user_id), loyalty_program_id=loyalty_program_id)