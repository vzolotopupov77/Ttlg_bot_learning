"""Настройки приложения из переменных окружения и .env."""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень репозитория (рядом с pyproject.toml), а не cwd — иначе .env не находится при другом каталоге запуска
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"
# Для диагностики в __main__ (путь к .env, без чтения секретов)
ENV_FILE_PATH = _ENV_FILE


class Settings(BaseSettings):
    """Конфигурация бота и LLM."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        # utf-8-sig: «Блокнот» на Windows часто пишет BOM — без этого ключ TELEGRAM_* не читается
        env_file_encoding="utf-8-sig",
        extra="ignore",
    )

    telegram_bot_token: str = Field(
        ...,
        description="Токен Telegram-бота",
    )

    @field_validator("telegram_bot_token")
    @classmethod
    def telegram_token_format(cls, value: str) -> str:
        """Тот же контракт, что у aiogram: без пробелов, вид `123456789:AAH...`."""
        token = value.strip()
        if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
            token = token[1:-1].strip()
        if any(ch.isspace() for ch in token):
            msg = "TELEGRAM_BOT_TOKEN не должен содержать пробелов"
            raise ValueError(msg)
        left, sep, right = token.partition(":")
        if token in ("your_token_here", "your_token", ""):
            msg = (
                "В .env всё ещё шаблон или пустое значение TELEGRAM_BOT_TOKEN. "
                "Замените строку на токен от @BotFather (формат цифры:строка), сохраните файл."
            )
            raise ValueError(msg)
        if not sep or not left.isdigit() or not right:
            msg = (
                "TELEGRAM_BOT_TOKEN неверного формата. Нужен токен от @BotFather вида "
                "123456789:AAH... Ровное имя переменной: TELEGRAM_BOT_TOKEN. "
                "Файл .env — в корне репозитория (рядом с pyproject.toml). "
                "Если в PowerShell переменная пустая — это нормально: значение берётся из .env."
            )
            raise ValueError(msg)
        return token

    openrouter_api_key: str = Field(
        ...,
        description="API-ключ OpenRouter",
    )
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="Базовый URL OpenAI-compatible API",
    )
    llm_model: str = Field(
        default="openai/gpt-4o-mini",
        description="Идентификатор модели в OpenRouter",
    )
    log_level: str = Field(default="INFO", description="Уровень логирования")
    history_depth: int = Field(
        default=20,
        ge=1,
        description="Глубина истории сообщений на пользователя",
    )
