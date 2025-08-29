from app.schemas.agent import AgentTypeEnum, AgentCategoryEnum
from app.agents.factory import create_agent

# Explicitly initialize all agents for registry
agent_registry = {
    (AgentTypeEnum.ANALYSIS_SUMMARY.name, AgentCategoryEnum.ORDER.name): create_agent(agent_type=AgentTypeEnum.ANALYSIS_SUMMARY.name.lower(), category=AgentCategoryEnum.ORDER.name.lower()),
    (AgentTypeEnum.ANALYSIS_SUMMARY.name, AgentCategoryEnum.CUSTOMER.name): create_agent(agent_type=AgentTypeEnum.ANALYSIS_SUMMARY.name.lower(), category=AgentCategoryEnum.CUSTOMER.name.lower()),
    (AgentTypeEnum.ANALYSIS_SUMMARY.name, AgentCategoryEnum.PRODUCT.name): create_agent(agent_type=AgentTypeEnum.ANALYSIS_SUMMARY.name.lower(), category=AgentCategoryEnum.PRODUCT.name.lower()),
    (AgentTypeEnum.STANDARD_COUPON.name, AgentCategoryEnum.ORDER.name): create_agent(agent_type=AgentTypeEnum.STANDARD_COUPON.name.lower(), category=AgentCategoryEnum.ORDER.name.lower()),
    (AgentTypeEnum.STANDARD_COUPON.name, AgentCategoryEnum.CUSTOMER.name): create_agent(agent_type=AgentTypeEnum.STANDARD_COUPON.name.lower(), category=AgentCategoryEnum.CUSTOMER.name.lower()),
    (AgentTypeEnum.STANDARD_COUPON.name, AgentCategoryEnum.PRODUCT.name): create_agent(agent_type=AgentTypeEnum.STANDARD_COUPON.name.lower(), category=AgentCategoryEnum.PRODUCT.name.lower()),
    (AgentTypeEnum.CHAT.name, AgentCategoryEnum.CHAT.name): create_agent(agent_type=AgentTypeEnum.CHAT.name.lower(), category=AgentCategoryEnum.CHAT.name.lower()),
    (AgentTypeEnum.RESEARCH.name, AgentCategoryEnum.RESEARCH.name): create_agent(agent_type=AgentTypeEnum.RESEARCH.name.lower(), category=AgentCategoryEnum.RESEARCH.name.lower()),
}

def get_agent(agent_type: str, agent_category: str):
    return agent_registry.get((agent_type, agent_category))