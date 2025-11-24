import asyncpg
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from pydantic_ai.agent import AgentRunResult
import asyncio
from app.crud.analysis_crud import analysis_crud
from app.crud.offer_crud import offer_crud
from app.schemas.core.enums import AnalysisTypeEnum
from app.agents.registry import get_agent
from typing import Dict, Any

async def generate_forecast(
    pool: asyncpg.Pool, 
    loyalty_program_id: int, 
    template_id: int  # ✅ Fixed typo
) -> Dict[str, Any]:
    """
    Generate forecast for a specific template's offers.
    
    Flow:
    1. Fetch customer analysis, order analysis, and latest offer data
    2. Build message history from these contexts
    3. Run forecast agent to predict offer performance
    4. Update the offer records with forecast data
    5. Return the forecast result
    """
    print(f"Starting forecast generation for template {template_id}, loyalty program {loyalty_program_id}")
    
    customer_analysis_result, order_analysis_result, offer_result = await asyncio.gather(
        analysis_crud.get_latest_analysis_result(
            pool=pool, 
            loyalty_program_id=loyalty_program_id, 
            analysis_type=AnalysisTypeEnum.CUSTOMER.value
        ),
        analysis_crud.get_latest_analysis_result(
            pool=pool, 
            loyalty_program_id=loyalty_program_id, 
            analysis_type=AnalysisTypeEnum.ORDER.value
        ),
        offer_crud.get_latest_offer(
            pool=pool, 
            loyalty_program_id=loyalty_program_id, 
            template_id=template_id
        )
    )
    
    message_history: list[ModelMessage] = []
    
    if customer_analysis_result:
        message_history.append(
            ModelResponse(parts=[TextPart(content=customer_analysis_result["analysis_json"])])
        )
    
    if order_analysis_result:
        message_history.append(
            ModelResponse(parts=[TextPart(content=order_analysis_result["analysis_json"])])
        )
    
    if offer_result:
        message_history.append(
            ModelResponse(parts=[TextPart(content=offer_result["pos_raw_data"])])
        )
    else:
        raise ValueError(f"No offer found for template {template_id}. Generate offers first.")
    
    user_prompt = f"Analyze the potential impact and forecast outcomes for these offers based on the customer and order analysis data."
    
    agent = get_agent(agent_type="forecast", agent_category="forecast")
    result = await agent.run(user_prompt=user_prompt, message_history=message_history)
    
    forecast_output = result.output
    
    updated_count = await offer_crud.update_forecast_for_template(
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        template_id=template_id,
        forecast_data=forecast_output.model_dump()
    )
    
    print(f"✓ Generated and saved forecast for template {template_id} ({updated_count} records updated)")
    
    return {
        "template_id": template_id,
        "loyalty_program_id": loyalty_program_id,
        "forecast": forecast_output.model_dump(),
        "records_updated": updated_count
    }