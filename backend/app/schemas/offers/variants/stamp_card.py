from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import FixedAmountDiscountDetails, FreebieDiscountDetails
from app.schemas.offers.eligibility_criteria import StampCardEligibility

class StampCardFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: StampCardEligibility

class StampCardFreebieOffer(BaseModel):
    discount: FreebieDiscountDetails
    eligibility: StampCardEligibility

class StampCardTemplate(BaseModel):
    """Container for stamp card/loyalty progression offers (offers 9, 10)."""
    fixed_offer: StampCardFixedOffer
    freebie_offer: StampCardFreebieOffer
    template_name: str = "STAMP_CARD"