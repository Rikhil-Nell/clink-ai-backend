from fastapi import APIRouter
from .routers import chat, analysis

router = APIRouter()

router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])