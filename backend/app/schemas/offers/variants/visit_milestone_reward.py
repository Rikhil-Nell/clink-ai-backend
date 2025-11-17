from pydantic import BaseModel, Field
from app.schemas.offers.discount_details import PercentageDiscountDetails, FixedAmountDiscountDetails, FreebieDiscountDetails
from app.schemas.offers.eligibility_criteria import FirstVisitEligibility, VisitMilestoneEligibility

class FirstVisitPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: FirstVisitEligibility

class FirstVisitFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: FirstVisitEligibility

class FirstVisitTemplate(BaseModel):
    """Container for first-time buyer offers (offers 7, 8)."""
    percentage_offer: FirstVisitPercentageOffer
    fixed_offer: FirstVisitFixedOffer
    template_name: str = "VISIT_MILESTONE_FIRST_VISIT"
    

class VisitBasedPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: VisitMilestoneEligibility

class VisitBasedFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: VisitMilestoneEligibility

class VisitBasedFreebieOffer(BaseModel):
    discount: FreebieDiscountDetails
    eligibility: VisitMilestoneEligibility

class VisitBasedTemplate(BaseModel):
    """Container for visit-based reward offers (offers 17, 18, 19)."""
    percentage_offer: VisitBasedPercentageOffer
    fixed_offer: VisitBasedFixedOffer
    freebie_offer: VisitBasedFreebieOffer
    template_name: str = "VISIT_MILESTONE_VISIT_BASED"
