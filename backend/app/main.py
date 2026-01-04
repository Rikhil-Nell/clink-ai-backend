from contextlib import asynccontextmanager

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis

from app.db.database import db_manager
from app.api.v2.api import router
from app.core.config import settings

logfire.configure(token=settings.LOGFIRE_TOKEN,
                  environment=settings.LOGFIRE_ENVIRONMENT,
                  console=None
                )

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db_manager.init_pool()
        app.state.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        logfire.info("App started with database and Redis connections.")
    except Exception as e:
        logfire.error("Failed to initialize connections", exc_info=e)
        raise
    yield
    try:
        await app.state.redis.aclose()
        await db_manager.close_pool()
        logfire.info("App shutdown.")
    except Exception as e:
        logfire.error(f"Error during shutdown", exc_info=e)

app = FastAPI(lifespan=lifespan, title="My Chat Service")
logfire.instrument_fastapi(app=app)
logfire.instrument_asyncpg()
logfire.instrument_pydantic_ai()
logfire.instrument_redis()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include the router from the api directory
app.include_router(router, prefix="/api/v2")