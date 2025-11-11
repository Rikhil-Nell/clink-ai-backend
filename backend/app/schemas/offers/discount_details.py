from pydantic import BaseModel, Field
from typing import Literal, Union, List, Optional
from datetime import time


class PercentageDiscountDetails(BaseModel):
    kind: Literal["percentage"] = "percentage"
    discount_percentage: float                               # e.g. 15 (%)
    max_discount_amount: Optional[float] = None
    minimum_purchase_amount: Optional[float] = None

class FixedAmountDiscountDetails(BaseModel):
    kind: Literal["fixed_amount"] = "fixed_amount"
    value: float                               # e.g. 100 (currency units)
    minimum_purchase_amount: Optional[float] = None
    max_discount_amount: Optional[float] = None  # keep if business wants a cap

class FreebieDiscountDetails(BaseModel):
    kind: Literal["freebie"] = "freebie"
    free_item_name: str
    minimum_purchase_amount: Optional[float] = None
    max_redemptions_item: Optional[int] = None

DiscountDetails = Union[
    PercentageDiscountDetails,
    FixedAmountDiscountDetails,
    FreebieDiscountDetails
]