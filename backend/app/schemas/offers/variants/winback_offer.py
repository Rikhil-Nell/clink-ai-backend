from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import WinbackEligibility
from app.schemas.core.forecast import ForecastResponse

class MissYouPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: WinbackEligibility

class MissYouFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: WinbackEligibility

class MissYouTemplate(BaseModel):
    """Container for Miss You coupon variants (offers 3, 4)."""
    template_name: str = "WINBACK_MISS_YOU"
    percentage_offer: MissYouPercentageOffer
    fixed_offer: MissYouFixedOffer
    forecast: ForecastResponse