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

class TemplateIdEnum(IntEnum):
    """Template IDs stored in DB."""
    BASIC_DISCOUNT = 1
    WINBACK_OFFER = 2
    VISIT_MILESTONE_REWARD = 3
    STAMP_CARD = 4
    HAPPY_HOURS = 5
    COMBO_OFFER = 6