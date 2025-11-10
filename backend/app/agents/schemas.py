from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional
from datetime import time
from app.schemas.discount_details_schema import PercentageDiscountDetails, FixedAmountDiscountDetails, FreebieDiscountDetails, DiscountDetails
from app.schemas.elgibility_criteria_schema import StandardEligibility, WinbackEligibility, TimeBasedEligibility, StampCardEligibility, EligibilityCriteria
from enum import Enum


class AnalysisSummaryResponse(BaseModel):
    summary: str = Field(description="A concise, data-driven summary of the key findings from the analysis.")
    recommendations: List[str] = Field(description="A list of actionable recommendations based on the summary.")

class OfferCouponResponse(BaseModel):
    offer_id: Optional[int] = None
    template_name: Optional[str] = None
    offer_title: str
    offer_channel_type: Literal[
        "coupon",          # hidden coupon code style
        "standard",        # always visible
        "time_based",      # appears only in a time window
        "missyou",         # winback / lapsed customer trigger
        "stamp_card",      # loyalty progress reward
        "freebie"          # free item style
    ]
    discount_details: DiscountDetails
    eligibility_criteria: EligibilityCriteria
    display_section: Literal["hidden", "standard", "highlight"] = "hidden"

class MissYouCouponPercentageOffer(BaseModel):
    discount: PercentageDiscountDetails
    eligibility: WinbackEligibility

class MissYouCouponFixedOffer(BaseModel):
    discount: FixedAmountDiscountDetails
    eligibility: WinbackEligibility

class MissYouCouponResponse(BaseModel):
    """Container for both Miss You coupon variants with individual eligibility criteria."""
    percentage_offer: MissYouCouponPercentageOffer = Field(
        description="Percentage-based Miss You offer with winback eligibility"
    )
    fixed_offer: MissYouCouponFixedOffer = Field(
        description="Fixed amount Miss You offer with winback eligibility"
    )
    template_name: str = Field(default="WINBACK_MISSYOU")

class Winback(Enum):
    MISS_YOU = MissYouCouponResponse

