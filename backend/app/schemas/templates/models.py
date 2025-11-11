from pydantic import BaseModel
from typing import Type

class TemplateConfig(BaseModel):
    """Minimal config for template lookup - customize fields as needed."""
    template_id: str
    agent_type: str      # "winback", "standard_coupon", etc.
    agent_category: str  # "MISS_YOU", "ORDER", etc.
    model_class: Type[BaseModel]
