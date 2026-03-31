"""HTTP-клиент к backend: диалог без прямого вызова LLM."""

from __future__ import annotations

import logging
from uuid import UUID

import httpx

logger = logging.getLogger(__name__)

MSG_SERVICE_DOWN = "Сервис временно недоступен. Попробуйте позже."
MSG_BAD_REQUEST = "Ошибка запроса. Обратитесь к администратору."
MSG_USER_NOT_FOUND = (
    "Профиль не найден. Попросите преподавателя зарегистрировать вас в системе."
)
MSG_DIALOGUE_NOT_FOUND = "Диалог не найден. Напишите снова — начнём новый."
MSG_LLM_UNAVAILABLE = "Ассистент временно недоступен. Попробуйте позже."
MSG_RATE_LIMIT = "Слишком много запросов. Подождите немного и повторите."


class BackendError(Exception):
    """Ошибка backend; user_message — текст для пользователя в Telegram."""

    def __init__(self, user_message: str) -> None:
        self.user_message = user_message
        super().__init__(user_message)


class BackendClient:
    """POST /v1/dialogue/message; хранит dialogue_id на пользователя в памяти процесса."""

    def __init__(
        self,
        *,
        base_url: str,
        timeout: float,
        _client: httpx.AsyncClient | None = None,
    ) -> None:
        self._base = base_url.rstrip("/")
        self._client = _client if _client is not None else httpx.AsyncClient(timeout=timeout)
        self._dialogues: dict[int, UUID] = {}

    async def aclose(self) -> None:
        await self._client.aclose()

    async def send_message(self, telegram_id: int, text: str) -> str:
        dialogue_id = self._dialogues.get(telegram_id)
        payload: dict = {
            "telegram_id": telegram_id,
            "text": text,
            "dialogue_id": str(dialogue_id) if dialogue_id else None,
        }
        url = f"{self._base}/v1/dialogue/message"
        try:
            response = await self._client.post(url, json=payload)
        except httpx.ConnectError as e:
            logger.warning("Backend unreachable: ConnectError %s", e)
            raise BackendError(MSG_SERVICE_DOWN) from e
        except httpx.TimeoutException as e:
            logger.warning("Backend timeout: %s", e)
            raise BackendError(MSG_SERVICE_DOWN) from e

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                logger.error("Backend returned invalid JSON (200)")
                raise BackendError(MSG_SERVICE_DOWN) from None
            reply = data.get("text")
            if not reply or not isinstance(reply, str):
                logger.error("Backend response missing text")
                raise BackendError(MSG_SERVICE_DOWN)
            did = data.get("dialogue_id")
            if did:
                try:
                    self._dialogues[telegram_id] = UUID(str(did))
                except ValueError:
                    logger.warning("Invalid dialogue_id in response: %s", did)
            return reply.strip()

        user_msg = _map_error_response(response)
        if response.status_code == 404 and _error_code(response) == "dialogue_not_found":
            self._dialogues.pop(telegram_id, None)
        logger.info(
            "Backend error status=%s code=%s",
            response.status_code,
            _error_code(response),
        )
        raise BackendError(user_msg)


def _error_code(response: httpx.Response) -> str | None:
    try:
        body = response.json()
        err = body.get("error") if isinstance(body, dict) else None
        if isinstance(err, dict):
            code = err.get("code")
            return str(code) if code is not None else None
    except ValueError:
        pass
    return None


def _map_error_response(response: httpx.Response) -> str:
    code = _error_code(response)
    if response.status_code == 404 and code == "user_not_found":
        return MSG_USER_NOT_FOUND
    if response.status_code == 404 and code == "dialogue_not_found":
        return MSG_DIALOGUE_NOT_FOUND
    if response.status_code == 503 and code == "llm_unavailable":
        return MSG_LLM_UNAVAILABLE
    if response.status_code == 429:
        return MSG_RATE_LIMIT
    try:
        body = response.json()
        err = body.get("error") if isinstance(body, dict) else None
        if isinstance(err, dict):
            msg = err.get("message")
            if isinstance(msg, str) and msg and response.status_code == 422:
                return "Запрос отклонён. Проверьте текст сообщения."
    except ValueError:
        pass
    if 400 <= response.status_code < 500:
        return MSG_BAD_REQUEST
    return MSG_SERVICE_DOWN
