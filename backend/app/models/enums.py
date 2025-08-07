# app/models/enums.py
from enum import Enum

class AnalysisType(str, Enum):
    CUSTOMER = "customer"
    ORDER = "order" 
    PRODUCT = "product"

class ChatRole(str, Enum):
    USER = "user"
    BOT = "bot"

class BotResponseType(str, Enum):
    RESEARCH_AGENT = "research_agent"
    CHAT_AGENT = "chat_agent"
    ANALYSIS_AGENT = "analysis_agent"
    COUPON_GENERATION_AGENT = "coupon_generation_agent"