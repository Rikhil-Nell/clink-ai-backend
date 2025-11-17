from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.schemas.core.enums import AgentTypeEnum

class ChatMessageBase(BaseModel):
    """The core fields for a chat message."""
    role: str
    content: str

class ChatMessageCreate(BaseModel):
    """The request body for sending a new message."""
    content: str
    agent_type: AgentTypeEnum
    agent_category: str = "chat"  # Only allow chat/research

class ChatMessageResponse(ChatMessageBase):
    """A single chat message returned to the frontend."""
    created_at: datetime

class ChatHistoryResponse(BaseModel):
    """The response body for the chat history endpoint."""
    history: List[ChatMessageResponse]