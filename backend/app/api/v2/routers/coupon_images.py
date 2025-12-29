from fastapi import APIRouter, Depends, HTTPException
import asyncpg

from app.api.deps import get_db_pool, AuthData, get_current_auth_data
from app.services.coupon_image_service import generate_coupon_image
from app.schemas.core.image_gen import CouponImageRequest, CouponImageResponse

router = APIRouter(prefix="/coupon-images", tags=["Coupon Images"])


@router.post("/generate", response_model=CouponImageResponse)
async def create_coupon_image(
    request: CouponImageRequest,
    auth: AuthData = Depends(get_current_auth_data),
    pool: asyncpg.Pool = Depends(get_db_pool)
):
    """
    Generate a coupon image for a selected offer variant.
    
    The frontend sends:
    - loyalty_program_id: To fetch the brand logo
    - order_id: The ai_suggestions row UUID
    - selected_offer: The specific variant (percentage/fixed/freebie) they chose
    - brand_name: The cafe/restaurant name
    - brand_colors: Optional hex color codes
    - style_config: Optional style preferences
    
    Returns the S3 URL of the generated image.
    """
    try:
        result = await generate_coupon_image(
            pool=pool,
            request=request,
            loyalty_program_id=auth.loyalty_program_id  # From auth, not request
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/regenerate/{s3_key:path}")
# async def regenerate_coupon_image(
#     s3_key: str,
#     request: CouponImageRequest,
#     prompt_adjustment: str = "",
#     pool: asyncpg.Pool = Depends(get_db_pool)
# ):
#     """
#     Regenerate an existing coupon image with optional prompt adjustments.
    
#     This allows users to request modifications like:
#     - "Make the colors warmer"
#     - "Add more festive elements"
#     - "Make the text larger"
#     """
#     # You could store the original request params and modify them
#     # For now, just regenerate with the new request
#     try:
#         result = await coupon_image_service.generate_coupon_image(pool, request)
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))