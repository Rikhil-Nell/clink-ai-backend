from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails
from app.schemas.offers.eligibility_criteria import StandardEligibility
from app.schemas.core.forecast import ForecastResponse

class ComboOfferPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: StandardEligibility

class ComboOfferFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: StandardEligibility

class ComboOfferTemplate(BaseModel):
    """Container for combo offer variants (offers 15, 16)."""
    template_name: str = "COMBO_OFFER"
    percentage_offer: ComboOfferPercentageOffer
    fixed_offer: ComboOfferFixedOffer
    forecast: ForecastResponse