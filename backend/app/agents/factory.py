from typing import Union, Optional, Tuple
from pydantic import BaseModel
from pydantic_ai import Agent

# Local Imports
from app.core.config import research_model, chat_model, analysis_model, coupon_model, default_model_settings
from app.agents.schemas import (
    AnalysisSummaryResponse,
    Winback
)

from app.agents.prompts import get_prompt


def create_agent(
    agent_type: str,
    category: Optional[str] = None
) -> Union[Agent, Agent[BaseModel]]:
    """
    Factory function to create an agent based on category and type.
    
    Args:
        agent_type: 'research', 'analysis_summary', 'standard_coupon', 'creative_coupon' or "chat".
        category: 'order', 'customer', or 'product'.
        
    Returns:
        A configured pydantic_ai Agent instance.
    """
    instructions = get_prompt(agent_type=agent_type, category=category)
    
    if agent_type == "analysis_summary":

        return Agent[AnalysisSummaryResponse](
            model=analysis_model,
            model_settings=default_model_settings,
            instructions=instructions,
            output_type=AnalysisSummaryResponse,
            instrument=True
        )
        
    elif agent_type == "winback":
        output_schema = Winback[category.upper()].value
        if not output_schema:
            raise ValueError(f"No standard coupon schema defined for category: {category}")

        return Agent[output_schema](
            model=coupon_model,
            model_settings=default_model_settings,
            instructions=instructions,
            output_type=output_schema
        )
        
    elif agent_type == "chat":

        return Agent(
            model=chat_model,
            model_settings=default_model_settings,
            instructions=instructions,
            instrument=True
        )
    
    elif agent_type == "research":

        return Agent(
            model=research_model,
            model_settings=default_model_settings,
            instructions=instructions,
            instrument=True
        ) 
    
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")