from fastapi import APIRouter
from .routers import analysis, offer, coupon_images

router = APIRouter()

router.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
router.include_router(offer.router, prefix="/offer", tags=["Offer"])
router.include_router(coupon_images.router, prefix="/coupon-images", tags=["Coupon Images"])