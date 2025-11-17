from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import StandardEligibility

class BasicCouponPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: StandardEligibility

class BasicCouponFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: StandardEligibility

class BasicCouponTemplate(BaseModel):
    """Container for hidden basic coupon variants (offers 1, 2)."""
    percentage_offer: BasicCouponPercentageOffer
    fixed_offer: BasicCouponFixedOffer
    template_name: str = "BASIC_DISCOUNT_COUPON"
    

class StandardCouponPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: StandardEligibility

class StandardCouponFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: StandardEligibility

class StandardCouponTemplate(BaseModel):
    """Container for standard display coupon variants (offers 11, 12)."""
    percentage_offer: StandardCouponPercentageOffer
    fixed_offer: StandardCouponFixedOffer
    template_name: str = "BASIC_DISCOUNT_STANDARD"
