import asyncpg
from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db_pool
from app.api.deps import get_current_auth_data
from app.services import chat_service
from app.schemas import *

router = APIRouter()

@router.post("/message_history")
async def get_chat_message(
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data)
):

    try:
        response_data = await chat_service.get_chat_history(
            pool=pool,
            loyalty_program_id=auth_data.loyalty_program_id,
        )
        return response_data
    except Exception as e:
        # You can add more specific error handling here
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chat")
async def chat(
    message: ChatMessageCreate,
    pool: asyncpg.Pool = Depends(get_db_pool),
    auth_data: AuthData = Depends(get_current_auth_data),
):
    
    try:
        response: ChatMessageResponse = await chat_service.chat(
            pool=pool,
            content=message.content,
            agent_type=message.agent_type,
            agent_category=message.agent_category,
            loyalty_program_id=auth_data.loyalty_program_id
        )
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 

