"""Интеграционные тесты BackendClient → FastAPI backend (in-memory SQLite, mock LLM).

Паттерн из fastapi-templates skill: httpx.AsyncClient + ASGITransport(app=app).
Проверяют весь путь бот → BackendClient → POST /v1/dialogue/message → ответ.
"""

from __future__ import annotations

import pytest

from ttlg_bot.services.backend_client import (
    BackendClient,
    BackendError,
    MSG_LLM_UNAVAILABLE,
    MSG_SERVICE_DOWN,
    MSG_USER_NOT_FOUND,
)

from tests.conftest import (
    TELEGRAM_ID_KNOWN,
    TELEGRAM_ID_UNKNOWN,
    _seed_student,
    make_bot_client,
)


@pytest.mark.usefixtures("backend_app")
async def test_send_message_success() -> None:
    """Успешный запрос: известный пользователь, mock LLM → ответ-строка."""
    client = make_bot_client()
    await _seed_student(client)

    reply = await client.send_message(TELEGRAM_ID_KNOWN, "Сколько будет 2+2?")

    assert isinstance(reply, str)
    assert len(reply) > 0
    await client.aclose()


@pytest.mark.usefixtures("backend_app")
async def test_dialogue_id_persisted_across_messages() -> None:
    """После первого сообщения dialogue_id сохраняется и используется во втором."""
    client = make_bot_client()
    await _seed_student(client)

    await client.send_message(TELEGRAM_ID_KNOWN, "Первый вопрос")
    dialogue_id_after_first = client._dialogues.get(TELEGRAM_ID_KNOWN)

    assert dialogue_id_after_first is not None, "dialogue_id не был сохранён после первого ответа"

    await client.send_message(TELEGRAM_ID_KNOWN, "Второй вопрос")
    dialogue_id_after_second = client._dialogues.get(TELEGRAM_ID_KNOWN)

    assert dialogue_id_after_second == dialogue_id_after_first, (
        "dialogue_id изменился между сообщениями — ожидалось продолжение диалога"
    )
    await client.aclose()


@pytest.mark.usefixtures("backend_app")
async def test_unknown_user_raises_backend_error_with_user_message() -> None:
    """Незарегистрированный пользователь → BackendError с текстом про профиль."""
    client = make_bot_client()

    with pytest.raises(BackendError) as exc_info:
        await client.send_message(TELEGRAM_ID_UNKNOWN, "Привет")

    assert exc_info.value.user_message == MSG_USER_NOT_FOUND
    await client.aclose()


@pytest.mark.usefixtures("backend_app")
async def test_empty_text_raises_backend_error() -> None:
    """Пустой текст → backend возвращает 422 → BackendError (не traceback в чат)."""
    client = make_bot_client()
    await _seed_student(client)

    with pytest.raises(BackendError):
        await client.send_message(TELEGRAM_ID_KNOWN, "   ")

    await client.aclose()


@pytest.mark.usefixtures("backend_app_llm_broken")
async def test_llm_unavailable_returns_friendly_message() -> None:
    """Backend отвечает 503 llm_unavailable → BackendError с текстом про ассистента."""
    client = make_bot_client()
    await _seed_student(client)

    with pytest.raises(BackendError) as exc_info:
        await client.send_message(TELEGRAM_ID_KNOWN, "Помоги решить задачу")

    assert exc_info.value.user_message == MSG_LLM_UNAVAILABLE
    await client.aclose()


@pytest.mark.usefixtures("backend_app")
async def test_invalid_dialogue_id_cleared_on_not_found() -> None:
    """Если dialogue_id устарел (404 dialogue_not_found) — он удаляется из кэша."""
    from uuid import uuid4

    client = make_bot_client()
    await _seed_student(client)
    client._dialogues[TELEGRAM_ID_KNOWN] = uuid4()

    with pytest.raises(BackendError):
        await client.send_message(TELEGRAM_ID_KNOWN, "Продолжить диалог")

    assert TELEGRAM_ID_KNOWN not in client._dialogues, (
        "dialogue_id должен быть удалён после 404 dialogue_not_found"
    )
    await client.aclose()


async def test_connect_error_raises_service_down(monkeypatch: pytest.MonkeyPatch) -> None:
    """ConnectError (backend не запущен) → BackendError с текстом 'сервис недоступен'."""
    import httpx

    client = BackendClient(base_url="http://127.0.0.1:19999", timeout=1.0)

    original_post = client._client.post

    async def _raise_connect(*_args: object, **_kwargs: object) -> None:
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(client._client, "post", _raise_connect)

    with pytest.raises(BackendError) as exc_info:
        await client.send_message(12345, "Тест")

    assert exc_info.value.user_message == MSG_SERVICE_DOWN
    await client.aclose()
