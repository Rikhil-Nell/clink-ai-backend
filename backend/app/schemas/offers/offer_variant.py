from typing import Literal, Optional, Union
from pydantic import BaseModel, Field
from uuid import UUID

from app.schemas.offers.discount_details import (
    PercentageDiscountDetails,
    FixedAmountDiscountDetails,
    FreebieDiscountDetails,
    DiscountDetails
)
from app.schemas.offers.eligibility_criteria import EligibilityCriteria


class OfferVariant(BaseModel):
    """A single offer variant with discount and eligibility."""
    discount: DiscountDetails
    eligibility: EligibilityCriteria


class PercentageOfferVariant(BaseModel):
    """Percentage-based offer variant."""
    discount: PercentageDiscountDetails
    eligibility: EligibilityCriteria


class FixedOfferVariant(BaseModel):
    """Fixed amount offer variant."""
    discount: FixedAmountDiscountDetails
    eligibility: EligibilityCriteria


class FreebieOfferVariant(BaseModel):
    """Freebie offer variant."""
    discount: FreebieDiscountDetails
    eligibility: EligibilityCriteria


# The payload the frontend sends for image generation
class SelectedOfferVariant(BaseModel):
    """
    The offer variant selected by the business owner for image generation.
    
    Frontend sends this along with order_id to specify which variant 
    they want to generate an image for.
    """
    template_name: str = Field(..., description="e.g., VISIT_MILESTONE_VISIT_BASED")
    variant_type: Literal["percentage_offer", "fixed_offer", "freebie_offer"]
    variant_data: OfferVariant
    
    def get_discount_text(self) -> str:
        """Generate human-readable discount text for the coupon image."""
        discount = self.variant_data.discount
        
        if discount.kind == "percentage":
            return f"{int(discount.discount_percentage)}% OFF"
        elif discount.kind == "fixed_amount":
            return f"₹{int(discount.value)} OFF"
        elif discount.kind == "freebie":
            return f"FREE {discount.free_item_name.upper()}"
        return "SPECIAL OFFER"
    
    def get_eligibility_text(self) -> str:
        """Generate human-readable eligibility/validity text."""
        eligibility = self.variant_data.eligibility
        
        if eligibility.kind == "visit_milestone":
            return f"Unlock after {eligibility.visit_count_required} visits"
        elif eligibility.kind == "first_visit":
            return "For first-time customers"
        elif eligibility.kind == "winback":
            return f"We miss you! Come back after {eligibility.days_since_last_visit}+ days"
        elif eligibility.kind == "time_based":
            return f"Valid {eligibility.valid_hours_start} - {eligibility.valid_hours_end}"
        elif eligibility.kind == "stamp_card":
            return f"Collect {eligibility.threshold_count} stamps"
        elif eligibility.kind == "standard":
            if eligibility.validity_period_days:
                return f"Valid for {eligibility.validity_period_days} days"
            return "Limited time offer"
        return ""