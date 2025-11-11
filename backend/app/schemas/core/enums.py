from enum import IntEnum

class AgentTypeEnum(IntEnum):
    """The types of agents the frontend can request, mapped to integers."""
    CHAT = 1
    RESEARCH = 2
    ANALYSIS_SUMMARY = 3
    WINBACK = 4

class AgentCategoryEnum(IntEnum):
    """Categories of Agents, mapped to integers."""
    CHAT = 1
    RESEARCH = 2
    CUSTOMER = 3
    ORDER = 4
    PRODUCT = 5
    MISS_YOU = 6

class MessageTypeEnum(IntEnum):
    """Cateogries of messages, mappeed to integers"""
    USER = 1
    BOT = 2
    SYSTEM = 3

class AnalysisTypeEnum(IntEnum):
    CUSTOMER = 1
    ORDER = 2
    PRODUCT = 3
