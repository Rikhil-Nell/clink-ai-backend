import os
import secrets
from enum import Enum
from typing import Any, Optional

from pydantic import PostgresDsn, EmailStr, field_validator, Field
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

# You'll need to install pydantic-ai for these
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIModelName, OpenAIChatModelSettings, OpenAIResponsesModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic_ai.models.google import GoogleModel, GoogleModelName, GoogleModelSettings

class Settings(BaseSettings):

    # --- Database Parts (loaded from .env) ---
    DATABASE_USER: str = Field(..., validation_alias="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(..., validation_alias="DATABASE_PASSWORD")
    DATABASE_HOST: str = Field(..., validation_alias="DATABASE_HOST")
    DATABASE_PORT: int = Field(..., validation_alias="DATABASE_PORT")
    DATABASE_NAME: str = Field(..., validation_alias="DATABASE_NAME")

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
    REDIS_URL: str = Field(..., validation_alias="REDIS_URL")

    # --- AWS ---
    AWS_ACCESS_KEY: str = Field(..., validation_alias="AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY: str = Field(..., validation_alias="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(..., validation_alias="AWS_REGION")
    S3_BUCKET: str = Field(default="clink-backend-staging", validation_alias="S3_BUCKET")

    # --- AI & Service Keys (loaded from .env) ---
    OPENAI_API_KEY: str = Field(..., validation_alias="OPENAI_API_KEY")
    # LOGFIRE_KEY: str
    PERPLEXITY_API_KEY: str = Field(..., validation_alias="PERPLEXITY_API_KEY")
    GOOGLE_API_KEY: str = Field(..., validation_alias="GOOGLE_API_KEY")

    # --- AI Model Configuration ---
    RESEARCH_MODEL_NAME: str = "sonar"
    ANALYSIS_MODEL_NAME: OpenAIModelName = "gpt-5"
    COUPON_MODEL_NAME: OpenAIModelName = "gpt-5"
    CHAT_MODEL_NAME: OpenAIModelName = "gpt-5-nano"
    FORECAST_MODEL_NAME: OpenAIModelName = "gpt-5"
    STENCIL_MODEL_NAME: OpenAIModelName = "gpt-5"
    IMAGE_GENERATION_MODEL_NAME: GoogleModelName = "gemini-3-pro-image-preview"
    
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
google_provider = GoogleProvider(api_key=settings.GOOGLE_API_KEY)

# Define Models
research_model = OpenAIChatModel(model_name=settings.RESEARCH_MODEL_NAME, provider=perplexity_provider, settings=default_model_settings)
analysis_model = OpenAIChatModel(model_name=settings.ANALYSIS_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
coupon_model = OpenAIChatModel(model_name=settings.COUPON_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
chat_model = OpenAIChatModel(model_name=settings.CHAT_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
forecast_model = OpenAIChatModel(model_name=settings.FORECAST_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
stencil_model = OpenAIResponsesModel(model_name=settings.STENCIL_MODEL_NAME, provider=openai_provider, settings=default_model_settings)
image_generation_model = GoogleModel(model_name=settings.IMAGE_GENERATION_MODEL_NAME, provider=google_provider, settings=default_model_settings)