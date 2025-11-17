from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import WinbackEligibility

class MissYouPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: WinbackEligibility

class MissYouFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: WinbackEligibility

class MissYouTemplate(BaseModel):
    """Container for Miss You coupon variants (offers 3, 4)."""
    percentage_offer: MissYouPercentageOffer
    fixed_offer: MissYouFixedOffer
    template_name: str = "WINBACK_MISSYOU"