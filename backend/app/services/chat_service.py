# in backend/app/services/chat_service.py

import asyncpg
from typing import Tuple, Any, Dict, Union
from app.agents.factory import create_agent, Agent
from app.agents.schemas import OrderStandardCouponResponse, CustomerStandardCouponResponse
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, UserPromptPart, TextPart

def initialize_agents() -> Tuple[Agent, Agent, Agent, Agent, Agent, Agent]:
    order_analysis_agent = create_agent(agent_type="analysis_summary", category="order")
    customer_analysis_agent = create_agent(agent_type="analysis_summary", category="customer")
    order_coupon_agent = create_agent(agent_type="standard_coupon", category="order")
    customer_coupon_agent = create_agent(agent_type="standard_coupon", category="customer")
    chat_agent = create_agent(agent_type="chat", category="chat")
    research_agent = create_agent(agent_type="research", category="research")
    return order_analysis_agent, customer_analysis_agent, order_coupon_agent, customer_coupon_agent, chat_agent, research_agent



async def process_user_message(pool: asyncpg.Pool, user_id: int, loyalty_id: int, message: str):
    """
    1. Fetches history from the DB using the provided pool.
    2. Calls the AI agent.
    3. Saves new messages back to the DB.
    """
    # Fetch conversation history
    history_query = "SELECT role, content FROM chat_messages WHERE loyalty_program_id = $1 ORDER BY created_at ASC;"
    async with pool.acquire() as conn:
        history_records = await conn.fetch(history_query, loyalty_id)
        history = [dict(rec) for rec in history_records]

    # Call your agent logic (placeholder)
    # agent = get_agent(history)
    # agent_response = await agent.get_response(message, history)
    agent_response = f"This is a placeholder response to your message: '{message}'" # Placeholder

    # Save messages to the database
    insert_query = "INSERT INTO chat_messages (loyalty_program_id, role, content, created_at) VALUES ($1, $2, $3, NOW());"
    async with pool.acquire() as conn:
        # Run inserts in a transaction for safety
        async with conn.transaction():
            await conn.execute(insert_query, loyalty_id, "user", message)
            await conn.execute(insert_query, loyalty_id, "bot", agent_response)
    
    return {"response": agent_response}