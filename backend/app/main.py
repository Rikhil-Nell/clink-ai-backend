from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.db.database import db_manager
from app.api.v2.api import router
# from app.agents.registry import initialize_agent_registry

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await db_manager.init_pool()
        logger.info("App started with database connection.")
    except Exception as e:
        logger.error(f"Failed to initialize database pool: {e}")
        raise
    yield
    try:
        await db_manager.close_pool()
        logger.info("App shutdown.")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

app = FastAPI(lifespan=lifespan, title="My Chat Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include the router from the api directory
app.include_router(router, prefix="/api/v2")