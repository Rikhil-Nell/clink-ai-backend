from fastapi import APIRouter
from app.api.v1.routers import analysis, chat

api_router = APIRouter()
api_router.include_router(router=analysis.router, prefix="/analysis", tags=["Analysis"])
api_router