from enum import IntEnum


class AgentTypeEnum(IntEnum):
    """High-level agent types."""
    CHAT = 1
    RESEARCH = 2
    ANALYSIS_SUMMARY = 3
    OFFER_GENERATION = 4


class AgentCategoryEnum(IntEnum):
    """Agent categories (sub-types)."""
    # Chat/Research
    CHAT = 1
    RESEARCH = 2
    
    # Analysis
    CUSTOMER = 3
    ORDER = 4
    PRODUCT = 5
    
    # Offer Templates
    COUPON = 6
    STANDARD = 7
    MISS_YOU = 8
    FIRST_VISIT = 9
    VISIT_BASED = 10
    LOYALTY = 11
    TIME_BASED = 12


class MessageTypeEnum(IntEnum):
    USER = 1
    BOT = 2
    SYSTEM = 3


class AnalysisTypeEnum(IntEnum):
    CUSTOMER = 1
    ORDER = 2
    PRODUCT = 3


class GoalEnum(IntEnum):
    INCREASE_AOV = 1
    REPEAT_CUSTOMERS = 2
    INCREASE_OCCUPANCY = 3


class TemplateEnum(IntEnum):
    """
    Template IDs - integers for API privacy.
    Maps to internal string template names.
    """
    BASIC_DISCOUNT_COUPON = 1
    BASIC_DISCOUNT_STANDARD = 2
    WINBACK_MISS_YOU = 3
    VISIT_MILESTONE_FIRST_VISIT = 4
    VISIT_MILESTONE_VISIT_BASED = 5
    STAMP_CARD_LOYALTY = 6
    HAPPY_HOURS_TIME_BASED = 7
    COMBO_OFFER_STANDARD = 8
    
    @property
    def template_name(self) -> str:
        """Get the internal string template name."""
        return self.name  # Returns "STANDARD_BASIC_DISCOUNT", etc.
    
    @classmethod
    def from_name(cls, name: str) -> "TemplateEnum":
        """Get enum from string name (for internal use)."""
        return cls[name]


# Lookup dict for quick int -> string conversion
TEMPLATE_ID_TO_NAME: dict[int, str] = {t.value: t.name for t in TemplateEnum}
TEMPLATE_NAME_TO_ID: dict[str, int] = {t.name: t.value for t in TemplateEnum}