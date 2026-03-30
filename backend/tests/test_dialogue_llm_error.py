"""Dialogue endpoint returns 503 when LLM fails."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from ttlg_backend.api.dialogue import get_llm_client
from ttlg_backend.config import get_settings
from ttlg_backend.db import ensure_sqlite_schema, init_db, reset_engine
from ttlg_backend.llm.errors import LLMUnavailableError
from ttlg_backend.main import app


@pytest.fixture
async def dialogue_client_llm_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[AsyncClient, None]:
    monkeypatch.setenv("TTLG_ALLOW_SQLITE_TEST", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    get_settings.cache_clear()
    await reset_engine()
    init_db(get_settings())
    await ensure_sqlite_schema(get_settings())

    class BoomLLM:
        async def complete_chat(self, *, system_prompt: str, user_message: str) -> str:
            raise LLMUnavailableError

    app.dependency_overrides[get_llm_client] = lambda: BoomLLM()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        cu = await ac.post(
            "/v1/users",
            json={"name": "S", "role": "student", "telegram_id": 999001},
        )
        assert cu.status_code == 201
        yield ac

    app.dependency_overrides.clear()


async def test_dialogue_llm_unavailable_returns_503(
    dialogue_client_llm_fails: AsyncClient,
) -> None:
    r = await dialogue_client_llm_fails.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999001, "text": "Q"},
    )
    assert r.status_code == 503
    assert r.json()["error"]["code"] == "llm_unavailable"
