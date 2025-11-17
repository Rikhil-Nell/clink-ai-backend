# from app.schemas.core.enums import AgentTypeEnum, AgentCategoryEnum
from typing import Dict, Tuple, Optional
from pydantic_ai import Agent
from app.agents.factory import create_agent

# Cache for instantiated agents (lazy initialization)
_agent_cache: Dict[Tuple[str, str], Agent] = {}

def get_agent(agent_type: str, agent_category: str) -> Optional[Agent]:
    """
    Get or create an agent for the given type/category.
    Agents are created lazily and cached.
    """
    key = (agent_type.lower(), agent_category.lower())
    
    if key not in _agent_cache:
        # Create and cache the agent
        _agent_cache[key] = create_agent(agent_type=agent_type, category=agent_category)
    
    return _agent_cache[key]

def clear_agent_cache():
    """Clear the agent cache (useful for testing or hot-reloading)."""
    _agent_cache.clear()