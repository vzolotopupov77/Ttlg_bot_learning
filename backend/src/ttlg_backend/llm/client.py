"""Async OpenAI-compatible client (OpenRouter)."""

from __future__ import annotations

import logging

from openai import APIError, APITimeoutError, AsyncOpenAI, RateLimitError

from ttlg_backend.config import Settings
from ttlg_backend.llm.errors import LLMUnavailableError

logger = logging.getLogger(__name__)


class LLMClient:
    """Thin wrapper around AsyncOpenAI with timeouts and error mapping."""

    def __init__(self, settings: Settings) -> None:
        key = settings.openrouter_api_key
        api_key = key.get_secret_value() if key else "missing-key"
        timeout = settings.llm_timeout_seconds
        self._model = settings.llm_model
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.openrouter_base_url.rstrip("/"),
            timeout=timeout,
        )

    @classmethod
    def from_settings(cls, settings: Settings) -> LLMClient:
        return cls(settings)

    async def complete_chat(self, *, system_prompt: str, user_message: str) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            )
        except APITimeoutError as exc:
            logger.warning("LLM request timed out: %s", type(exc).__name__)
            raise LLMUnavailableError from exc
        except RateLimitError as exc:
            logger.warning("LLM rate limited: %s", type(exc).__name__)
            raise LLMUnavailableError from exc
        except APIError as exc:
            logger.warning("LLM API error: %s", type(exc).__name__)
            raise LLMUnavailableError from exc
        except Exception as exc:  # noqa: BLE001 — map unexpected provider errors
            logger.warning("LLM unexpected error: %s", type(exc).__name__)
            raise LLMUnavailableError from exc

        choice = response.choices[0].message.content
        if not choice:
            raise LLMUnavailableError
        return choice.strip()
