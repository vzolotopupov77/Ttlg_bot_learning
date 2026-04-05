"""Dialogue endpoint returns 503 when LLM fails."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.dialogue import get_llm_client
from ttlg_backend.config import get_settings
from ttlg_backend.db import get_session
from ttlg_backend.llm.errors import LLMUnavailableError
from ttlg_backend.main import app


@pytest.fixture
async def dialogue_client_llm_fails(
    pg_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    get_settings.cache_clear()

    async def _override() -> AsyncGenerator[AsyncSession, None]:
        yield pg_session

    class BoomLLM:
        async def complete_chat(self, *, system_prompt: str, user_message: str) -> str:
            raise LLMUnavailableError

    app.dependency_overrides[get_session] = _override
    app.dependency_overrides[get_llm_client] = lambda: BoomLLM()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        cu = await ac.post(
            "/v1/users",
            json={"name": "S", "role": "student", "telegram_id": 999001},
        )
        assert cu.status_code == 201
        yield ac

    app.dependency_overrides.pop(get_session, None)
    app.dependency_overrides.pop(get_llm_client, None)
    get_settings.cache_clear()


async def test_dialogue_llm_unavailable_returns_503(
    dialogue_client_llm_fails: AsyncClient,
) -> None:
    r = await dialogue_client_llm_fails.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999001, "text": "Q"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "llm_unavailable"
