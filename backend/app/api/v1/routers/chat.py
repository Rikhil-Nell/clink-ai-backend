# in backend/app/api/v1/routers/chat.py

import asyncpg
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.db.database import get_db_pool
from backend.app.api.deps import get_current_user_id
from backend.app.services import chat_service # Business logic lives here

router = APIRouter()

class UserMessage(BaseModel):
    content: str
    loyalty_program_id: int

@router.post("/message")
async def handle_chat_message(
    message: UserMessage,
    pool: asyncpg.Pool = Depends(get_db_pool),           # <-- Gets the DB pool
    user_id: int = Depends(get_current_user_id)          # <-- Protects the endpoint
):
    """
    Handles a new incoming chat message from a user.
    The endpoint itself is very simple. All the work is done in the service.
    """
    try:
        response_data = await chat_service.process_user_message(
            pool=pool,
            user_id=user_id,
            loyalty_id=message.loyalty_program_id,
            message=message.content
        )
        return response_data
    except Exception as e:
        # You can add more specific error handling here
        raise HTTPException(status_code=500, detail=str(e))