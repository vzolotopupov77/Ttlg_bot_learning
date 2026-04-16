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

    secret_key: str = Field(
        ...,
        min_length=1,
        description="Secret for signing JWT (HS256). Must be non-empty.",
    )
    access_token_expire_minutes: int = Field(
        default=60,
        gt=0,
        description="JWT lifetime in minutes; must be > 0.",
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

    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        description="Comma-separated origins for browser CORS (Next.js dev on another port).",
    )

    # Сид преподавателя (backend/scripts/seed.py); читаются из .env
    teacher_name: str = Field(
        default="Преподаватель",
        description="Отображаемое имя учителя при make backend-db-seed",
    )
    teacher_email: str = Field(
        default="teacher@local.dev",
        description="Email для POST /v1/auth/login после сида",
    )
    teacher_default_password: SecretStr | None = Field(
        default=None,
        description="Пароль для сида dev; bcrypt в БД",
    )

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
        msg = "DATABASE_URL must use postgresql+asyncpg:// (or sqlite+aiosqlite:// with TTLG_ALLOW_SQLITE_TEST=1)"
        raise ValueError(msg)

    @field_validator("secret_key", mode="before")
    @classmethod
    def reject_empty_secret_key(cls, v: object) -> str:
        if v is None:
            msg = "SECRET_KEY is required"
            raise ValueError(msg)
        s = str(v).strip()
        if not s:
            msg = "SECRET_KEY must not be empty"
            raise ValueError(msg)
        return s


@lru_cache
def get_settings() -> Settings:
    return Settings()
