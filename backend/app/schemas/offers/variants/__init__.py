from app.schemas.offers.variants.basic_discount import BasicCouponTemplate, StandardCouponTemplate
from app.schemas.offers.variants.combo_offer import ComboOfferTemplate 
from app.schemas.offers.variants.happy_hours import HappyHoursTemplate
from app.schemas.offers.variants.stamp_card import StampCardTemplate
from app.schemas.offers.variants.visit_milestone_reward import FirstVisitTemplate, VisitBasedTemplate
from app.schemas.offers.variants.winback_offer import MissYouTemplate

__all__ = [
    "BasicCouponTemplate",
    "StandardCouponTemplate",
    "ComboOfferTemplate",
    "HappyHoursTemplate",
    "StampCardTemplate",
    "FirstVisitTemplate",
    "VisitBasedTemplate",
    "MissYouTemplate",
]