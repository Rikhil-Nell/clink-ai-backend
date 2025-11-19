from pydantic_ai.messages import ModelMessage
from pydantic_ai.agent import AgentRunResult
from app.agents.registry import get_agent
from typing import List
import json

async def get_forecast(message_history: List[ModelMessage]) -> AgentRunResult:

    agent = get_agent(agent_type="forecast", agent_category="forecast")
    result = await agent.run(user_prompt="", message_history=message_history)
    return result