"""Диалог с LLM: системный промпт, история, вызов клиента."""

from __future__ import annotations

import logging
from openai import APIError, APITimeoutError, RateLimitError

from ttlg_bot.services.history import HistoryStore
from ttlg_bot.services.llm_client import LLMClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Ты — помощник по математике (алгебра, геометрия, подготовка к ОГЭ, 7–9 класс). "
    "Отвечай ясно и по делу. Если вопрос вне твоей роли — вежливо откажись."
)

USER_ERROR_SHORT = "Сервис временно недоступен. Попробуйте позже."
USER_ERROR_RATE = "Слишком много запросов. Подождите немного и повторите."


class ChatService:
    def __init__(self, history: HistoryStore, llm: LLMClient) -> None:
        self._history = history
        self._llm = llm

    async def reply(self, user_id: int, user_text: str) -> str:
        self._history.add(user_id, "user", user_text)

        api_messages: list[dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *list(self._history.messages_for_api(user_id)),
        ]

        try:
            answer = await self._llm.chat(api_messages)
        except RateLimitError:
            self._history.pop_last(user_id)
            return USER_ERROR_RATE
        except (APITimeoutError, APIError, ValueError) as e:
            logger.exception("LLM failure for user_id=%s: %s", user_id, type(e).__name__)
            self._history.pop_last(user_id)
            return USER_ERROR_SHORT

        self._history.add(user_id, "assistant", answer)
        return answer
