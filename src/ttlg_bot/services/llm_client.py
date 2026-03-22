"""Тонкий клиент к OpenRouter через OpenAI-compatible API."""

from __future__ import annotations

import logging
from collections.abc import Sequence

from openai import APIError, APITimeoutError, AsyncOpenAI, RateLimitError

logger = logging.getLogger(__name__)


class LLMClient:
    """Обёртка над AsyncOpenAI с base_url и моделью из конфига."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        timeout: float = 60.0,
    ) -> None:
        self._model = model
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url.rstrip("/"),
            timeout=timeout,
        )

    async def chat(
        self,
        messages: Sequence[dict[str, str]],
    ) -> str:
        """
        Вызов chat completions. messages — список с ролями system/user/assistant.

        При ошибке API бросает исключение; короткий текст для пользователя — на уровне сервиса.
        """
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=list(messages),
            )
        except RateLimitError as e:
            logger.warning("LLM rate limit: %s", e)
            raise
        except APITimeoutError as e:
            logger.warning("LLM timeout: %s", e)
            raise
        except APIError as e:
            logger.warning("LLM API error: %s", e)
            raise

        choice = response.choices[0] if response.choices else None
        if not choice or not choice.message.content:
            logger.error("LLM empty response")
            raise ValueError("Пустой ответ модели")

        return choice.message.content.strip()
