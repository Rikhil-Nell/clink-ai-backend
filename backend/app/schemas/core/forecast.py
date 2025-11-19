from pydantic import BaseModel, Field

class ForecastResponse(BaseModel):
    target: int = Field(description="How much the restaurant is projected to earn after using this particular coupon strategy")
    budget: int = Field(description="How much money would they need to spend to implement these discounts")
    predicted_redemptions: int = Field(description="How many redemptions of this discount might occur")
    roi: str = Field(description="based on the budget and target give a value like (2x, 4x, 5x) and such")