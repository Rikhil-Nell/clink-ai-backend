# schemas/offers/variants/miss_you.py
from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import WinbackEligibility

class MissYouCouponPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: WinbackEligibility

class MissYouCouponFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: WinbackEligibility

class MissYouTemplate(BaseModel):
    """Container for both Miss You coupon variants."""
    percentage_offer: MissYouCouponPercentageOffer
    fixed_offer: MissYouCouponFixedOffer
    template_name: str = "WINBACK_MISSYOU"