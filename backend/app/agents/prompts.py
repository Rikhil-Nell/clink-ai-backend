from pathlib import Path

def get_prompt(agent_type: str, category: str) -> str:
    """
    Dynamically loads a prompt from a text file.
    
    Args:
        agent_type: The type of agent (e.g., 'analysis_summary', 'basic_discount', 'winback').
        category: The category of the agent (e.g., 'order', 'customer', 'coupon', 'miss_you').
        
    Returns:
        The content of the prompt file as a string.
        
    Raises:
        FileNotFoundError: If the prompt file doesn't exist.
    """
    prompt_file = Path(f"app/agents/prompts/{agent_type}/{category}_prompt.txt")
    
    if not prompt_file.exists():
        raise FileNotFoundError(
            f"Prompt file not found at: {prompt_file}\n"
            f"Expected structure: app/agents/prompts/{agent_type}/{category}_prompt.txt"
        )
    
    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read()