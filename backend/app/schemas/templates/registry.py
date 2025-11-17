from typing import Dict, List
from app.schemas.offers.variants import (
    BasicCouponTemplate,
    StandardCouponTemplate,
    ComboOfferTemplate,
    HappyHoursTemplate,
    StampCardTemplate,
    FirstVisitTemplate,
    VisitBasedTemplate,
    MissYouTemplate,
)
from app.schemas.templates.models import TemplateConfig
from app.schemas.core.enums import GoalEnum, TemplateIdEnum
from typing import Optional

TEMPLATE_REGISTRY: Dict[str, TemplateConfig] = {
    # BASIC DISCOUNT TEMPLATES (Goal 1: AOV, Goal 3: Occupancy)
    "BASIC_DISCOUNT_COUPON": TemplateConfig(
        template_id=TemplateIdEnum.BASIC_DISCOUNT.value,
        agent_type="basic_discount",
        agent_category="coupon",
        model_class=BasicCouponTemplate,
        goal_ids=[GoalEnum.INCREASE_AOV.value, GoalEnum.INCREASE_OCCUPANCY.value]
    ),
    "BASIC_DISCOUNT_STANDARD": TemplateConfig(
        template_id=TemplateIdEnum.BASIC_DISCOUNT.value,
        agent_type="basic_discount",
        agent_category="standard",
        model_class=StandardCouponTemplate,
        goal_ids=[GoalEnum.INCREASE_AOV.value, GoalEnum.INCREASE_OCCUPANCY.value]
    ),
    
    # WINBACK TEMPLATE (Goal 2: Retention)
    "WINBACK_MISS_YOU": TemplateConfig(
        template_id=TemplateIdEnum.WINBACK_OFFER.value,
        agent_type="winback",
        agent_category="miss_you",
        model_class=MissYouTemplate,
        goal_ids=[GoalEnum.REPEAT_CUSTOMERS.value]
    ),
    
    # VISIT MILESTONE TEMPLATES
    # First Visit: Goal 3 (Acquisition)
    "VISIT_MILESTONE_FIRST_VISIT": TemplateConfig(
        template_id=TemplateIdEnum.VISIT_MILESTONE_REWARD.value,
        agent_type="visit_milestone",
        agent_category="first_visit",
        model_class=FirstVisitTemplate,
        goal_ids=[GoalEnum.INCREASE_OCCUPANCY.value]
    ),
    # Visit-Based: Goal 2 (Retention)
    "VISIT_MILESTONE_VISIT_BASED": TemplateConfig(
        template_id=TemplateIdEnum.VISIT_MILESTONE_REWARD.value,
        agent_type="visit_milestone",
        agent_category="visit_based",
        model_class=VisitBasedTemplate,
        goal_ids=[GoalEnum.REPEAT_CUSTOMERS.value]
    ),
    
    # STAMP CARD TEMPLATE (Goal 2: Retention)
    "STAMP_CARD_LOYALTY": TemplateConfig(
        template_id=TemplateIdEnum.STAMP_CARD.value,
        agent_type="stamp_card",
        agent_category="loyalty",
        model_class=StampCardTemplate,
        goal_ids=[GoalEnum.REPEAT_CUSTOMERS.value]
    ),
    
    # HAPPY HOURS TEMPLATE (Goal 3: Occupancy)
    "HAPPY_HOURS_TIME_BASED": TemplateConfig(
        template_id=TemplateIdEnum.HAPPY_HOURS.value,
        agent_type="happy_hours",
        agent_category="time_based",
        model_class=HappyHoursTemplate,
        goal_ids=[GoalEnum.INCREASE_OCCUPANCY.value]
    ),
    
    # COMBO OFFER TEMPLATE (Goal 1: AOV)
    "COMBO_OFFER_STANDARD": TemplateConfig(
        template_id=TemplateIdEnum.COMBO_OFFER.value,
        agent_type="combo_offer",
        agent_category="standard",
        model_class=ComboOfferTemplate,
        goal_ids=[GoalEnum.INCREASE_AOV.value]
    ),
}

def get_template_config(template_id: str) -> TemplateConfig:
    if template_id not in TEMPLATE_REGISTRY:
        raise ValueError(f"Unknown template: {template_id}")
    return TEMPLATE_REGISTRY[template_id]

def get_template_config_by_id(template_id: int) -> Optional[TemplateConfig]:
    """Get template config by integer ID (for DB lookups)."""
    for config in TEMPLATE_REGISTRY.values():
        if config.template_id == template_id:
            return config
    return None

def get_all_template_ids() -> List[str]:
    """Returns list of all registered template IDs."""
    return list(TEMPLATE_REGISTRY.keys())

def get_templates_by_goal(goal_id: int) -> List[TemplateConfig]:
    """Returns all templates that map to a specific goal."""
    return [
        config for config in TEMPLATE_REGISTRY.values()
        if goal_id in config.goal_ids
    ]