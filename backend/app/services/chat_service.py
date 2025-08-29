import asyncpg
import asyncio
from datetime import datetime
from typing import List, Dict
from app.schemas import ChatMessageResponse
from app.agents.registry import get_agent
from app.utils.message_parser import parser
from app.crud.chat_crud import chat_crud
from app.crud.analysis_crud import analysis_crud
from app.schemas import AnalysisTypeEnum, AgentTypeEnum, AgentCategoryEnum, MessageTypeEnum
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart

async def chat(pool: asyncpg.Pool, content: str, agent_type: AgentTypeEnum, agent_category: AgentCategoryEnum, loyalty_program_id: int) -> ChatMessageResponse:
    
    messages = await chat_crud.fetch_chat_history(pool=pool, loyalty_program_id=loyalty_program_id)
    message_history: list[ModelMessage] = await parser(messages)

    tasks = [
        analysis_crud.get_latest_analysis_result(pool=pool, loyalty_program_id=loyalty_program_id, analysis_type=AnalysisTypeEnum.CUSTOMER.value),
        analysis_crud.get_latest_analysis_result(pool=pool, loyalty_program_id=loyalty_program_id, analysis_type=AnalysisTypeEnum.ORDER.value),
    #    analysis_crud.get_latest_analysis_result(pool=pool, loyalty_program_id=loyalty_program_id, analysis_type=AnalysisTypeEnum.PRODUCT.value)
    ]

    customer_analysis_result, order_analysis_result = await asyncio.gather(*tasks)
    # customer_analysis_result, order_analysis_result, product_analysis_result = await asyncio.gather(*tasks)
    customer_analysis = customer_analysis_result["analysis_json"] if customer_analysis_result else None
    order_analysis = order_analysis_result["analysis_json"] if order_analysis_result else None
    # product_analysis = product_analysis_result["analysis_json"] if product_analysis_result else None

    message_history.append(ModelResponse(parts=[TextPart(content=customer_analysis)]))
    message_history.append(ModelResponse(parts=[TextPart(content=order_analysis)]))
    # message_history.append(ModelResponse(parts=[TextPart(content=product_analysis)]))

    agent = get_agent(agent_type.name, agent_category.name)

    response = await agent.run(user_prompt=content, message_history=message_history)

    await chat_crud.insert_chat_message(pool=pool, loyalty_program_id=loyalty_program_id, role=MessageTypeEnum.USER.value, agent_type=agent_type.value, agent_category=agent_category.value, content=content)
    await chat_crud.insert_chat_message(pool=pool, loyalty_program_id=loyalty_program_id, role=MessageTypeEnum.BOT.value, agent_type=agent_type.value, agent_category=agent_category.value, content=response.output)

    chat_message_response = ChatMessageResponse(
        role="bot",
        content=response.output,
        created_at=datetime.utcnow()
    )
    return chat_message_response
    
async def get_chat_history(pool: asyncpg.Pool, loyalty_program_id) -> List[Dict]:
    message_history = await chat_crud.fetch_chat_history(pool=pool, loyalty_program_id=loyalty_program_id)
    return message_history