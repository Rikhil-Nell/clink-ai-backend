from typing import Dict, Type
from app.schemas.offers.variants.miss_you import MissYouTemplate
# from app.schemas.offers.variants.basic_discount import BasicDiscountTemplate
from app.schemas.templates.models import TemplateConfig


TEMPLATE_REGISTRY: Dict[str, TemplateConfig] = {
    "WINBACK_MISS_YOU": TemplateConfig(
        template_id="WINBACK_MISS_YOU",
        agent_type="WINBACK",
        agent_category="MISS_YOU",
        model_class=MissYouTemplate
    ),
    # "BASIC_DISCOUNT": TemplateConfig(
    #     template_id="BASIC_DISCOUNT",
    #     agent_type="standard_coupon",
    #     agent_category="order",
    #     model_class=BasicDiscountTemplate
    # ),
    # Add more as you build them
}

def get_template_config(template_id: str) -> TemplateConfig:
    if template_id not in TEMPLATE_REGISTRY:
        raise ValueError(f"Unknown template: {template_id}")
    return TEMPLATE_REGISTRY[template_id]