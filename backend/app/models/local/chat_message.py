import uuid as uuid_pkg
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from app.models.enums import ChatRole, BotResponseType

class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True, index=True)
    role: ChatRole
    content: str
    bot_response_type: Optional[BotResponseType] = None
    loyalty_program_id: uuid_pkg.UUID = Field(foreign_key="loyalty_programs.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))