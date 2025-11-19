from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import TimeBasedEligibility

class HappyHoursPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: TimeBasedEligibility

class HappyHoursFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: TimeBasedEligibility

class HappyHoursTemplate(BaseModel):
    """Container for time-based happy hours offers (offers 13, 14)."""
    template_name: str = "HAPPY_HOURS"
    percentage_offer: HappyHoursPercentageOffer
    fixed_offer: HappyHoursFixedOffer