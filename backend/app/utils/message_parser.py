from typing import List, Dict
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, UserPromptPart, TextPart

async def parser(messaages: List[Dict]) -> List[ModelMessage]:
    message_history: List[ModelMessage] = []

    for item in messaages:
        role = item["role"]
        content = item["content"]

        if role == "user":
            message_history.append(ModelRequest(parts=[UserPromptPart(content=content)]))
        elif role == "bot":
            message_history.append(ModelResponse(parts=[TextPart(content=content)]))
            
    return message_history
