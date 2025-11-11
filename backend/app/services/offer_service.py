import asyncpg
import asyncio
from typing import Optional
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart

from app.schemas.templates.registry import TEMPLATE_REGISTRY, get_template_config
from app.agents.registry import get_agent
from app.crud.analysis_crud import analysis_crud
from app.crud.offer_crud import offer_crud
from app.schemas.core.enums import AnalysisTypeEnum

async def _run_one_template_generation(
    template_id: str,
    pool: asyncpg.Pool,
    loyalty_program_id: int,
):
    """
    Generate offers for ONE template and save to DB.
    Parallel to `_run_one_analysis` in analysis_service.
    """
    print(f"Running template generation for: {template_id}")
    
    
    template_config = get_template_config(template_id)
    agent = get_agent(template_config.agent_type, template_config.agent_category)
    
    if not agent:
        raise LookupError(f"Could not find the agent with the template ID: {template_id}")

    message_history: list[ModelMessage] = []

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

    user_prompt = f"Generate offers for loyalty program {loyalty_program_id}"
    
    result = await agent.run(user_prompt=user_prompt)
    generated_offers = result.output
    
    await offer_crud.save_template_offers(
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        template_id=template_id,
        offers_data=generated_offers.model_dump()
    )
    
    print(f"✓ Saved {template_id} offers to DB")
    return generated_offers


async def generate_one_template(
    pool: asyncpg.Pool,
    loyalty_program_id: int,
    template_id: str,
    context: Optional[dict] = None
):
    """
    Public API: Generate ONE template.
    Usage: await generate_one_template(pool, 11, "WINBACK_MISSYOU")
    """
    return await _run_one_template_generation(pool, loyalty_program_id, template_id, context)


async def generate_all_templates(
    pool: asyncpg.Pool,
    loyalty_program_id: int,
    context: Optional[dict] = None
):
    """
    Public API: Generate ALL registered templates in parallel.
    Parallel to `trigger_all_analyses` in analysis_service.
    """
    print(f"Starting all template generations for loyalty program: {loyalty_program_id}")
    
    tasks = [
        _run_one_template_generation(pool, loyalty_program_id, template_id, context)
        for template_id in TEMPLATE_REGISTRY.keys()
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Log any failures
    for template_id, result in zip(TEMPLATE_REGISTRY.keys(), results):
        if isinstance(result, Exception):
            print(f"✗ Failed to generate {template_id}: {result}")
        else:
            print(f"✓ Generated {template_id}")
    
    print("All template generations completed")
    return results