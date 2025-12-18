import os
import secrets
from enum import Enum
from typing import Any, Optional

from pydantic import PostgresDsn, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

# You'll need to install pydantic-ai for these
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIModelName, OpenAIChatModelSettings



class Settings(BaseSettings):

    # --- Database Parts (loaded from .env) ---
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    # --- Computed Database URI ---
    # This field will be assembled by the validator below
    ASYNC_DATABASE_URI: str = None

    @field_validator("ASYNC_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info: FieldValidationInfo) -> Any:
        if isinstance(v, str) and v:
            return v  # If the full URI is provided directly, use it
        
        # Otherwise, build it from the parts
        return str(PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("DATABASE_USER"),
            password=info.data.get("DATABASE_PASSWORD"),
            host=info.data.get("DATABASE_HOST"),
            port=info.data.get("DATABASE_PORT"),
            path=info.data.get("DATABASE_NAME"),
        ))

    # --- Redis ---
    REDIS_URL: str

    # --- AI & Service Keys (loaded from .env) ---
    OPENAI_API_KEY: str
    # LOGFIRE_KEY: str
    PERPLEXITY_API_KEY: str

    # --- AI Model Configuration ---
    RESEARCH_MODEL_NAME: str = "sonar"
    ANALYSIS_MODEL_NAME: OpenAIModelName = "gpt-5"
    COUPON_MODEL_NAME: OpenAIModelName = "gpt-5"
    CHAT_MODEL_NAME: OpenAIModelName = "gpt-5-nano"
    FORECAST_MODEL_NAME: OpenAIModelName = "gpt-5"
    
    MODEL_TEMPERATURE: float = 0.1
    MODEL_TOP_P: float = 0.95

    # --- Pydantic Settings Config ---
    # It's common to place the .env file in the project root
    model_config = SettingsConfigDict(case_sensitive=True, env_file="../.env", extra="ignore")

# --- Initialize a single settings object ---
settings = Settings()

# --- Initialize Global AI Objects using the settings ---

# Define shared model settings
default_model_settings = OpenAIChatModelSettings(
    temperature=settings.MODEL_TEMPERATURE,
    top_p=settings.MODEL_TOP_P
)

# Define providers
openai_provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)
perplexity_provider = OpenAIProvider(base_url='https://api.perplexity.ai', api_key=settings.PERPLEXITY_API_KEY)

# Define Models
research_model = OpenAIChatModel(model_name=settings.RESEARCH_MODEL_NAME, provider=perplexity_provider, settings=default_model_settings)
analysis_model = OpenAIChatModel(model_name=settings.ANALYSIS_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
coupon_model = OpenAIChatModel(model_name=settings.COUPON_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
chat_model = OpenAIChatModel(model_name=settings.CHAT_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
forecast_model = OpenAIChatModel(model_name=settings.FORECAST_MODEL_NAME, provider=openai_provider, settings=default_model_settings)