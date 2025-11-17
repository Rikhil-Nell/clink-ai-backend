import asyncpg
import asyncio
from typing import Optional
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart

from app.schemas.templates.registry import TEMPLATE_REGISTRY, get_template_config
from app.agents.registry import get_agent
from app.crud.analysis_crud import analysis_crud
from app.crud.offer_crud import offer_crud
from app.schemas.core.enums import AnalysisTypeEnum
from app.schemas.templates.models import TemplateConfig

async def _run_one_template_generation(
    template: TemplateConfig,
    pool: asyncpg.Pool,
    loyalty_program_id: int,
    user_prompt: str,
    message_history: list[ModelMessage]
):
    """
    Generate offers for ONE template and save to DB.
    """
    template_name = template.model_class.model_fields['template_name'].default

    print(f"Running template generation for: {template_name}")

    # Get agent (lazily created and cached)
    agent = get_agent(template.agent_type, template.agent_category)
    
    if not agent:
        raise LookupError(f"Could not create agent for template: {template_name}")

    # Run agent
    result = await agent.run(user_prompt=user_prompt, message_history=message_history)
    generated_offers = result.output
    
    # Save to DB with goal mappings
    inserted_ids = await offer_crud.save_template_offers(
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        template_id=template.template_id,
        goal_ids=template.goal_ids,  # Pass goal mappings
        offers_data=generated_offers.model_dump()
    )
    
    print(f"✓ Saved {template_name} offers to DB (IDs: {inserted_ids})")
    return generated_offers


async def generate_one_template(
    pool: asyncpg.Pool,
    loyalty_program_id: int,
    template_id: int,
    user_prompt: Optional[str] = None,
    message_history: Optional[list[ModelMessage]] = None
):
    """
    Public API: Generate ONE template.
    """
    if user_prompt is None:
        user_prompt = f"Generate offers for loyalty program {loyalty_program_id}"
    if message_history is None:
        message_history = []
    
    return await _run_one_template_generation(
        template_id=template_id,
        pool=pool,
        loyalty_program_id=loyalty_program_id,
        user_prompt=user_prompt,
        message_history=message_history
    )


async def generate_all_templates(
    pool: asyncpg.Pool,
    loyalty_program_id: int
):
    """
    Public API: Generate ALL registered templates in parallel.
    """
    print(f"Starting all template generations for loyalty program: {loyalty_program_id}")
    
    # Fetch analysis context
    customer_analysis_result, order_analysis_result = await asyncio.gather(
        analysis_crud.get_latest_analysis_result(pool=pool, loyalty_program_id=loyalty_program_id, analysis_type=AnalysisTypeEnum.CUSTOMER.value),
        analysis_crud.get_latest_analysis_result(pool=pool, loyalty_program_id=loyalty_program_id, analysis_type=AnalysisTypeEnum.ORDER.value),
    )
    
    # Build message history from analysis results
    message_history: list[ModelMessage] = []
    if customer_analysis_result:
        message_history.append(ModelResponse(parts=[TextPart(content=customer_analysis_result["analysis_json"])]))
    if order_analysis_result:
        message_history.append(ModelResponse(parts=[TextPart(content=order_analysis_result["analysis_json"])]))
    
    user_prompt = f"Generate offers for loyalty program {loyalty_program_id} based on the analysis data."
    
    # Generate all templates in parallel
    tasks = [
        _run_one_template_generation(
            template=template,
            pool=pool,
            loyalty_program_id=loyalty_program_id,
            user_prompt=user_prompt,
            message_history=message_history
        )
        for template in TEMPLATE_REGISTRY.values()
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Log results
    for template_id, result in zip(TEMPLATE_REGISTRY.keys(), results):
        if isinstance(result, Exception):
            print(f"✗ Failed to generate {template_id}: {result}")
        else:
            print(f"✓ Generated {template_id}")
    
    print("All template generations completed")
    return results