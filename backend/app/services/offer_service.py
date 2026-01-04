import asyncpg
import asyncio
import uuid

import logfire
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart

from app.schemas.templates.registry import TEMPLATE_REGISTRY, get_template_config
from app.schemas.templates.models import TemplateConfig
from app.schemas.core.enums import AnalysisTypeEnum
from app.agents.registry import get_agent
from app.crud.analysis_crud import analysis_crud
from app.crud.offer_crud import offer_crud
from app.utils.offer_forecast_splitter import separate_forecast_from_offers


@logfire.instrument("generate_all_templates for {loyalty_program_id}")
async def generate_all_templates(
    pool: asyncpg.Pool,
    loyalty_program_id: int
):
    """
    Public API: Generate ALL registered templates in parallel.
    """
    message_history = await _fetch_analysis_context(pool, loyalty_program_id)
    
    user_prompt = (
        f"Generate offers for loyalty program {loyalty_program_id} based on the analysis data. "
        f"Include a forecast for each offer showing target revenue, budget needed, predicted redemptions, and ROI."
    )
    
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
    
    # Log summary
    success_count = sum(1 for r in results if not isinstance(r, Exception))
    logfire.info(
        "All templates completed",
        total=len(results),
        success=success_count,
        failed=len(results) - success_count
    )
    
    return results


@logfire.instrument("fetch_analysis_context for {loyalty_program_id}")
async def _fetch_analysis_context(
    pool: asyncpg.Pool,
    loyalty_program_id: int
) -> list[ModelMessage]:
    """Fetch customer and order analysis to build message history."""
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
    """Generate offers for ONE template and save to DB."""
    template_name = template.model_class.model_fields['template_name'].default

    # Use span here because we need template_name (computed inside)
    with logfire.span(
        "generate template {template_name}",
        template_name=template_name,
        template_id=template.template_id,
        generation_uuid=generation_uuid
    ):
        agent = get_agent(template.agent_type, template.agent_category)
        
        if not agent:
            logfire.error("Agent not found", template_name=template_name)
            raise LookupError(f"Could not create agent for template: {template_name}")

        result = await agent.run(user_prompt=user_prompt, message_history=message_history)
        generated_offers = result.output
        
        full_data = generated_offers.model_dump()
        forecast_data, offers_data = separate_forecast_from_offers(full_data)
        
        inserted_ids = await offer_crud.save_template_offers(
            pool=pool,
            loyalty_program_id=loyalty_program_id,
            template_id=template.template_id,
            goal_ids=template.goal_ids,
            offers_data=offers_data,
            forecast_data=forecast_data,
            generation_uuid=generation_uuid
        )
        
        logfire.info(
            "Offers saved",
            template_name=template_name,
            offer_count=len(inserted_ids) if inserted_ids else 0
        )
        
        return generated_offers


@logfire.instrument("generate_one_template {template_id}")
async def generate_one_template(
    template_id: str,
    pool: asyncpg.Pool,
    loyalty_program_id: int,
):
    """Public API: Generate ONE template."""
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


