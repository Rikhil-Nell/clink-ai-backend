import os
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import PostgresDsn, EmailStr, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any
import secrets
from enum import Enum

class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"

class Settings(BaseSettings):
    MODE: ModeEnum = ModeEnum.development
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str

    # For JWT auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = secrets.token_urlsafe(32)

    # Database parts
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str

    # Computed Database URI
    ASYNC_DATABASE_URI: PostgresDsn | str = ""

    @field_validator("ASYNC_DATABASE_URI", mode="after")
    def assemble_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str) and v == "":
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=info.data.get("DATABASE_USER"),
                password=info.data.get("DATABASE_PASSWORD"),
                host=info.data.get("DATABASE_HOST"),
                port=info.data.get("DATABASE_PORT"),
                path=info.data.get("DATABASE_NAME"),
            )
        return v

    # For initial admin user creation
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    model_config = SettingsConfigDict(case_sensitive=True, env_file="../.env")


settings = Settings()