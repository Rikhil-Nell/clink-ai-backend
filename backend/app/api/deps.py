from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.database import AsyncSessionLocal

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session for a single API request.
    
    This uses a context manager to ensure the session is always closed
    after the request is finished, even if an error occurs.
    """
    async with AsyncSessionLocal() as session:
        yield session