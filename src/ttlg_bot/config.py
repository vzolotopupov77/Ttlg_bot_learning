"""Настройки приложения из переменных окружения и .env."""

from pathlib import Path

from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень репозитория (рядом с pyproject.toml), а не cwd — иначе .env не находится при другом каталоге запуска
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_FILE = _PROJECT_ROOT / ".env"
# Для диагностики в __main__ (путь к .env, без чтения секретов)
ENV_FILE_PATH = _ENV_FILE


class Settings(BaseSettings):
    """Конфигурация бота (Telegram + HTTP к backend)."""

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

    backend_url: HttpUrl = Field(
        ...,
        description="Базовый URL backend (например http://127.0.0.1:8000)",
    )

    backend_timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=300.0,
        description="Таймаут HTTP к backend, секунды",
    )

    log_level: str = Field(default="INFO", description="Уровень логирования")
