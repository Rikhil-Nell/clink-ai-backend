from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional
from datetime import time

class StandardEligibility(BaseModel):
    kind: Literal["standard"] = "standard"
    max_redemptions: Optional[int] = None
    validity_period_days: Optional[int] = None

class WinbackEligibility(BaseModel):
    kind: Literal["winback"] = "winback"
    days_since_last_visit: int
    max_redemptions: Optional[int] = None
    validity_period_days: Optional[int] = None

class TimeBasedEligibility(BaseModel):
    kind: Literal["time_based"] = "time_based"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    days_of_week: Optional[List[int]] = None        # 0=Mon ... 6=Sun
    max_redemptions: Optional[int] = None
    validity_period_days: Optional[int] = None

class StampCardEligibility(BaseModel):
    kind: Literal["stamp_card"] = "stamp_card"
    required_visits: int
    validity_period_days: Optional[int] = None
    max_redemptions: Optional[int] = None

EligibilityCriteria = Union[
    StandardEligibility,
    WinbackEligibility,
    TimeBasedEligibility,
    StampCardEligibility
]