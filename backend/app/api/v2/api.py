from fastapi import APIRouter
from .routers import analysis, offer

router = APIRouter()

router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
router.include_router(offer.router, prefix="/offer", tags=["Offer"])