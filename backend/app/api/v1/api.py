from fastapi import APIRouter
from .routers import chat, analysis, offer

router = APIRouter()

router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
router.include_router(offer.router, prefix="/offer", tags=["Offer"])