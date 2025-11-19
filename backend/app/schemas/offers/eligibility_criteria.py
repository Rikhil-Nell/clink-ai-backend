from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional
from datetime import time

class StandardEligibility(BaseModel):
    """Standard offers: Basic discount with redemption limits."""
    kind: Literal["standard"] = "standard"
    max_redemptions: Optional[int] = Field(None, description="Maximum number of times this offer can be redeemed")
    validity_period_days: Optional[int] = Field(None, description="Number of days the offer is valid for")

class WinbackEligibility(BaseModel):
    """Win-back offers: Target customers who haven't visited recently."""
    kind: Literal["winback"] = "winback"
    days_since_last_visit: int = Field(description="Minimum days since customer's last visit to be eligible")
    max_redemptions: Optional[int] = None
    validity_period_days: Optional[int] = None

class TimeBasedEligibility(BaseModel):
    """Happy Hours: Offers valid only during specific times/days."""
    kind: Literal["time_based"] = "time_based"
    valid_hours_start: str = Field(description="Start time for offer validity (e.g., 15:00)")
    valid_hours_end: str = Field(description="End time for offer validity (e.g., 18:00)")
    valid_days: List[int] = Field(description="Days of week when valid (0=Mon, 6=Sun)")
    applies_to: Optional[Literal["food_only", "beverages_only", "all"]] = Field(default="all")
    max_redemptions: Optional[int] = None
    validity_period_days: Optional[int] = None

class FirstVisitEligibility(BaseModel):
    """First-time buyer offers: Triggered after customer's first purchase."""
    kind: Literal["first_visit"] = "first_visit"
    trigger_event: Literal["after_first_visit"] = "after_first_visit"
    validity_period_days: Optional[int] = Field(None, description="Days after first visit when offer is valid")

class StampCardEligibility(BaseModel):
    """Stamp card / loyalty progression offers."""
    kind: Literal["stamp_card"] = "stamp_card"
    required_item: Optional[str] = Field(None, description="Specific item required for stamp (e.g., 'coffee')")
    required_tier: Optional[str] = Field(None, description="Customer tier required (e.g., 'gold', 'silver')")
    threshold_count: int = Field(description="Number of stamps/purchases required")
    window_duration_days: Optional[int] = Field(None, description="Time window to collect stamps")

class VisitMilestoneEligibility(BaseModel):
    """Visit-based rewards: Triggered after N visits."""
    kind: Literal["visit_milestone"] = "visit_milestone"
    visit_count_required: int = Field(description="Number of visits required to unlock this offer")
    max_redemptions: Optional[int] = Field(None, description="How many times they can redeem after unlocking")

EligibilityCriteria = Union[
    StandardEligibility,
    WinbackEligibility,
    TimeBasedEligibility,
    FirstVisitEligibility,
    StampCardEligibility,
    VisitMilestoneEligibility
]