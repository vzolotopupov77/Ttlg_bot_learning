"""Application settings (pydantic-settings)."""

from __future__ import annotations

from functools import lru_cache
from typing import Self

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed configuration. Secrets are never logged as plain text."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str | None = Field(
        default=None,
        description="Async SQLAlchemy URL (postgresql+asyncpg://...). If unset, API starts without DB.",
    )
    openrouter_api_key: SecretStr | None = Field(
        default=None,
        description="OpenRouter API key (required when calling real LLM)",
    )
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
    )
    llm_model: str = Field(default="openai/gpt-4o-mini")
    llm_timeout_seconds: float = Field(default=30.0, ge=1.0, le=300.0)
    log_level: str = Field(default="INFO")
    allow_sqlite_test: bool = Field(
        default=False,
        validation_alias="TTLG_ALLOW_SQLITE_TEST",
        description="If true, allow sqlite+aiosqlite:// URLs (tests only).",
    )

    @field_validator("allow_sqlite_test", mode="before")
    @classmethod
    def parse_allow_sqlite(cls, v: object) -> bool:
        if v is True or v is False:
            return v
        if v is None:
            return False
        s = str(v).strip().lower()
        return s in ("1", "true", "yes")

    @field_validator("database_url", mode="before")
    @classmethod
    def empty_database_url_as_none(cls, v: object) -> str | None:
        if v is None or v == "":
            return None
        s = str(v).strip()
        return s or None

    @model_validator(mode="after")
    def validate_database_url_scheme(self) -> Self:
        v = self.database_url
        if v is None:
            return self
        if v.startswith("postgresql+asyncpg://"):
            return self
        if v.startswith("sqlite+aiosqlite://") and self.allow_sqlite_test:
            return self
        msg = (
            "DATABASE_URL must use postgresql+asyncpg:// "
            "(or sqlite+aiosqlite:// with TTLG_ALLOW_SQLITE_TEST=1)"
        )
        raise ValueError(msg)


@lru_cache
def get_settings() -> Settings:
    return Settings()
