from typing import Union, Optional
from pydantic import BaseModel
from pydantic_ai import Agent, ImageGenerationTool, BinaryImage

# Local Imports
from app.core.config import research_model, chat_model, analysis_model, coupon_model, forecast_model, stencil_model, image_generation_model, default_model_settings
from app.schemas.core.analysis import AnalysisSummaryResponse
from app.schemas.core.forecast import ForecastResponse
from app.agents.prompts import get_prompt
from app.schemas.templates.registry import get_template_config, TEMPLATE_REGISTRY


def create_agent(
    agent_type: str,
    category: Optional[str] = None
) -> Union[Agent, Agent[BaseModel]]:
    """
    Factory function to create an agent based on type and category.
    
    For offer generation agents, uses TEMPLATE_REGISTRY to get the output schema.
    For non-offer agents (chat, research, analysis), uses hardcoded schemas.
    
    Args:
        agent_type: 'research', 'analysis_summary', 'chat', or template agent types
                   ('basic_discount', 'winback', 'stamp_card', etc.)
        category: For analysis: 'order', 'customer', 'product'
                 For offers: matches template_id components ('coupon', 'miss_you', etc.)
        
    Returns:
        A configured pydantic_ai Agent instance.
    """
    
    # === SPECIAL AGENTS (non-template) ===
    
    if agent_type == "analysis_summary":
        instructions = get_prompt(agent_type=agent_type, category=category)
        return Agent[AnalysisSummaryResponse](
            model=analysis_model,
            model_settings=default_model_settings,
            instructions=instructions,
            output_type=AnalysisSummaryResponse,
            instrument=True
        )
        
    elif agent_type == "chat":
        instructions = get_prompt(agent_type=agent_type, category="chat")
        return Agent(
            model=chat_model,
            model_settings=default_model_settings,
            instructions=instructions,
            instrument=True
        )
    
    elif agent_type == "research":
        instructions = get_prompt(agent_type=agent_type, category="research")
        return Agent(
            model=research_model,
            model_settings=default_model_settings,
            instructions=instructions,
            instrument=True
        )
    
    elif agent_type == "forecast":
        instructions = get_prompt(agent_type=agent_type, category="forecast")
        return Agent(
            model=forecast_model,
            model_settings=default_model_settings,
            instructions=instructions,
            output_type=ForecastResponse,
            instrument=True
        )

    elif agent_type == "forecast":
        instructions = get_prompt(agent_type=agent_type, category="forecast")
        return Agent(
            model=forecast_model,
            model_settings=default_model_settings,
            instructions=instructions,
            output_type=ForecastResponse,
            instrument=True
        )
    
    elif agent_type == "stencil":
        instructions = get_prompt(agent_type=agent_type, category="stencil")
        return Agent(
            model=stencil_model,
            model_settings=default_model_settings,
            instructions=instructions,
            builtin_tools=[
                ImageGenerationTool(
                    background='transparent',
                    input_fidelity='high',
                    moderation='low',
                    output_compression=100,
                    output_format='png',
                    # partial_images=3,
                    quality='high',
                    size='1024x1024',
                )],
            output_type=BinaryImage,
            instrument=True
        )
    
    elif agent_type == "image_generation":
        instructions = get_prompt(agent_type=agent_type, category="image_generation")
        return Agent(
            model=image_generation_model,
            model_settings=default_model_settings,
            instructions=instructions,
            builtin_tools=[
                ImageGenerationTool(
                    background='transparent',
                    input_fidelity='high',
                    moderation='low',
                    output_compression=100,
                    output_format='png',
                    # partial_images=3,
                    quality='high',
                    size='1024x1024',
                )],
            output_type=BinaryImage,
            instrument=True
        )
    

    # === TEMPLATE-DRIVEN OFFER AGENTS ===
    
    else:
        # Construct template_id from agent_type + category
        template_id = _construct_template_id(agent_type, category)
        
        if template_id not in TEMPLATE_REGISTRY:
            raise ValueError(f"Unknown agent type/category: {agent_type}/{category}. No matching template found.")
        
        template_config = get_template_config(template_id)
        output_schema = template_config.model_class
        instructions = get_prompt(agent_type=agent_type, category=category)
        
        return Agent[output_schema](
            model=coupon_model,
            model_settings=default_model_settings,
            instructions=instructions,
            output_type=output_schema,
            retries=3,
            instrument=True
        )


def _construct_template_id(agent_type: str, category: Optional[str]) -> str:
    """
    Constructs a template_id from agent_type and category.
    
    Examples:
        ('basic_discount', 'coupon') -> 'BASIC_DISCOUNT_COUPON'
        ('winback', 'miss_you') -> 'WINBACK_MISS_YOU'
        ('stamp_card', 'loyalty') -> 'STAMP_CARD_LOYALTY'
        ('happy_hours', 'time_based') -> 'HAPPY_HOURS_TIME_BASED'
        ('combo_offer', 'standard') -> 'COMBO_OFFER_STANDARD'
    """
    if not category:
        return agent_type.upper()
    
    return f"{agent_type.upper()}_{category.upper()}"