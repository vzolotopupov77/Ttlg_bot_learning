"""Диалог через backend API."""

from __future__ import annotations

import logging

from ttlg_bot.services.backend_client import BackendClient, BackendError

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, backend: BackendClient) -> None:
        self._backend = backend

    async def reply(self, user_id: int, user_text: str) -> str:
        try:
            return await self._backend.send_message(user_id, user_text)
        except BackendError as e:
            return e.user_message
        except Exception:
            logger.exception("Unexpected error for user_id=%s", user_id)
            return "Произошла ошибка. Попробуйте ещё раз."
