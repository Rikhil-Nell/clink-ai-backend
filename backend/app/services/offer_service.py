import asyncpg
import asyncio
import uuid
from typing import Optional
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart

from app.schemas.templates.registry import TEMPLATE_REGISTRY, get_template_config
from app.schemas.templates.models import TemplateConfig
from app.schemas.core.enums import AnalysisTypeEnum
from app.agents.registry import get_agent
from app.crud.analysis_crud import analysis_crud
from app.crud.offer_crud import offer_crud
from app.utils.offer_forecast_splitter import separate_forecast_from_offers

async def generate_all_templates(
    pool: asyncpg.Pool,
    loyalty_program_id: int
):
    """
    Public API: Generate ALL registered templates in parallel.
    Each template gets its own generation_uuid for retrieval.
    """
    print(f"Starting all template generations for loyalty program: {loyalty_program_id}")
    
    # Fetch analysis context once (shared across all templates)
    message_history = await _fetch_analysis_context(pool, loyalty_program_id)
    
    user_prompt = (
        f"Generate offers for loyalty program {loyalty_program_id} based on the analysis data. "
        f"Include a forecast for each offer showing target revenue, budget needed, predicted redemptions, and ROI."
    )
    
    # Generate all templates in parallel, each with its own UUID
    tasks = [
        _run_one_template_generation(
            template=template,
            pool=pool,
            loyalty_program_id=loyalty_program_id,
            user_prompt=user_prompt,
            message_history=message_history,
            generation_uuid=str(uuid.uuid4())
        )
        for template in TEMPLATE_REGISTRY.values()
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Log results
    for template_key, result in zip(TEMPLATE_REGISTRY.keys(), results):
        if isinstance(result, Exception):
            print(f"✗ Failed to generate {template_key}: {result}")
        else:
            print(f"✓ Generated {template_key}")
    
    print("All template generations completed")
    return results

async def _fetch_analysis_context(
    pool: asyncpg.Pool,
    loyalty_program_id: int
) -> list[ModelMessage]:
    """
    Fetch customer and order analysis to build message history.
    Shared by both single and batch generation.
    """
    customer_analysis_result, order_analysis_result = await asyncio.gather(
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
    
    return message_history


async def _run_one_template_generation(
    template: TemplateConfig,
    pool: asyncpg.Pool,
    loyalty_program_id: int,
    user_prompt: str,
    message_history: list[ModelMessage],
    generation_uuid: str
):
    """
    Generate offers for ONE template and save to DB.
    Now generates forecast data inline to reduce API calls.
    """
    template_name = template.model_class.model_fields['template_name'].default

    print(f"Running template generation for: {template_name}")

    # Get agent (lazily created and cached)
    agent = get_agent(template.agent_type, template.agent_category)
    
    if not agent:
        raise LookupError(f"Could not create agent for template: {template_name}")

    # Run agent (now generates both offers AND forecast)
    result = await agent.run(user_prompt=user_prompt, message_history=message_history)
    generated_offers = result.output
    
    # Extract forecast data and offers data separately
    full_data = generated_offers.model_dump()
    forecast_data, offers_data = separate_forecast_from_offers(full_data)
    
    # Save to DB with generation_uuid for grouping
    inserted_ids = await offer_crud.save_template_offers(
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        template_id=template.template_id,
        goal_ids=template.goal_ids,
        offers_data=offers_data,
        forecast_data=forecast_data,
        generation_uuid=generation_uuid
    )
    
    print(f"✓ Saved {template_name} offers to DB (IDs: {inserted_ids}, UUID: {generation_uuid})")
    return generated_offers


async def generate_one_template(
    template_id: str,
    pool: asyncpg.Pool,
    loyalty_program_id: int,
):
    """
    Public API: Generate ONE template.
    Now properly fetches analysis context if not provided.
    """
    
    generation_uuid = str(uuid.uuid4())
    
    message_history = await _fetch_analysis_context(pool, loyalty_program_id)
    
    user_prompt = (
        f"Generate offers for loyalty program {loyalty_program_id} based on the analysis data. "
        f"Include a forecast for each offer showing target revenue, budget needed, predicted redemptions, and ROI."
    )
    
    template = get_template_config(template_id)
    
    return await _run_one_template_generation(
        template=template,
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        user_prompt=user_prompt,
        message_history=message_history,
        generation_uuid=generation_uuid
    )


