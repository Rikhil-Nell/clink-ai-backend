from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List

class AgentType(str, Enum):
    """The types of agents the frontend can request."""
    chat = "chat"
    research = "research"
    coupon = "standard_coupon"
    analysis = "analysis_summary"

class AgentCategory(str,Enum):
    """Categories of Agents"""
    chat = "chat"
    research = "research"
    customer = "customer"
    order = "order"
    product = "product"

class ChatMessageBase(BaseModel):
    """The core fields for a chat message."""
    role: str
    content: str

class ChatMessageCreate(BaseModel):
    """The request body for sending a new message."""
    content: str
    agent_type: AgentType
    category: AgentCategory

class ChatMessageResponse(ChatMessageBase):
    """A single chat message returned to the frontend."""
    created_at: datetime

class ChatHistoryResponse(BaseModel):
    """The response body for the chat history endpoint."""
    history: List[ChatMessageResponse]