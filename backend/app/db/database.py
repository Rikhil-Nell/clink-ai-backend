import asyncpg
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)
logger = logging.getLogger("uvicorn.error")

class DatabaseManager:
    def __init__(self):
        self.pool: Optional[asyncpg.pool.Pool] = None
   
    async def init_pool(self):
        self.pool = await asyncpg.create_pool(
            dsn=settings.ASYNC_DATABASE_URI,
            min_size=5,
            max_size=20
        )
        logger.info("Database connection pool initialized.")
   
    async def close_pool(self):
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed.")
   
    def get_pool(self) -> asyncpg.pool.Pool:
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        return self.pool

db_manager = DatabaseManager()

async def get_db_pool() -> asyncpg.pool.Pool:
    return db_manager.get_pool()