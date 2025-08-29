from pydantic import BaseModel
from datetime import datetime
from enum import IntEnum
from typing import List

class AgentTypeEnum(IntEnum):
    """The types of agents the frontend can request, mapped to integers."""
    CHAT = 1
    RESEARCH = 2
    STANDARD_COUPON = 3
    ANALYSIS_SUMMARY = 4

class AgentCategoryEnum(IntEnum):
    """Categories of Agents, mapped to integers."""
    CHAT = 1
    RESEARCH = 2
    CUSTOMER = 3
    ORDER = 4
    PRODUCT = 5

class MessageTypeEnum(IntEnum):
    """Cateogries of messages, mappeed to integers"""
    USER = 1
    BOT = 2
    SYSTEM = 3

class ChatMessageBase(BaseModel):
    """The core fields for a chat message."""
    role: str
    content: str

class ChatMessageCreate(BaseModel):
    """The request body for sending a new message."""
    content: str
    agent_type: AgentTypeEnum
    agent_category: AgentCategoryEnum

class ChatMessageResponse(ChatMessageBase):
    """A single chat message returned to the frontend."""
    created_at: datetime

class ChatHistoryResponse(BaseModel):
    """The response body for the chat history endpoint."""
    history: List[ChatMessageResponse]