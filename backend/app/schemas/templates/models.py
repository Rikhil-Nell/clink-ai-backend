from pydantic import BaseModel
from typing import Type, List

class TemplateConfig(BaseModel):
    """Minimal config for template lookup."""
    template_id: int
    agent_type: str      # "winback", "basic_discount", etc.
    agent_category: str  # "miss_you", "coupon", etc.
    model_class: Type[BaseModel]
    goal_ids: List[int]  # Maps to GoalEnum values (e.g., [1, 3])
    
    class Config:
        arbitrary_types_allowed = True
