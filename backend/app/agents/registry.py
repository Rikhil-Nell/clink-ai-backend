from app.agents.factory import create_agent
from app.schemas.agent import AgentType, AgentCategory

# Explicitly initialize agents for registry
agent_registry = {
    (AgentType.analysis.value, AgentCategory.order.value): create_agent(agent_type=AgentType.analysis.value, category=AgentCategory.order.value),
    (AgentType.analysis.value, AgentCategory.customer.value): create_agent(agent_type=AgentType.analysis.value, category=AgentCategory.customer.value),
    (AgentType.analysis.value, AgentCategory.product.value): create_agent(agent_type=AgentType.analysis.value, category=AgentCategory.product.value),
    (AgentType.coupon.value, AgentCategory.order.value): create_agent(agent_type=AgentType.coupon.value, category=AgentCategory.order.value),
    (AgentType.coupon.value, AgentCategory.customer.value): create_agent(agent_type=AgentType.coupon.value, category=AgentCategory.customer.value),
    (AgentType.coupon.value, AgentCategory.product.value): create_agent(agent_type=AgentType.coupon.value, category=AgentCategory.product.value),
    (AgentType.chat.value, AgentCategory.chat.value): create_agent(agent_type=AgentType.chat.value, category=AgentCategory.chat.value),
    (AgentType.research.value, AgentCategory.research.value): create_agent(agent_type=AgentType.research.value, category=AgentCategory.research.value),
}

def get_agent(agent_type: str, category: str):
    agent = agent_registry.get((agent_type, category))
    return agent