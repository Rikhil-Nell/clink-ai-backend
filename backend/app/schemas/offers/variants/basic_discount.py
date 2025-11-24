from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import StandardEligibility
from app.schemas.core.forecast import ForecastResponse

class BasicCouponPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: StandardEligibility

class BasicCouponFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: StandardEligibility

class BasicCouponTemplate(BaseModel):
    """Container for hidden basic coupon variants (offers 1, 2)."""
    template_name: str = "BASIC_DISCOUNT_COUPON"
    percentage_offer: BasicCouponPercentageOffer
    fixed_offer: BasicCouponFixedOffer
    forecast: ForecastResponse
    

class StandardCouponPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: StandardEligibility

class StandardCouponFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: StandardEligibility

class StandardCouponTemplate(BaseModel):
    """Container for standard display coupon variants (offers 11, 12)."""
    template_name: str = "BASIC_DISCOUNT_STANDARD"
    percentage_offer: StandardCouponPercentageOffer
    fixed_offer: StandardCouponFixedOffer
    forecast: ForecastResponse
