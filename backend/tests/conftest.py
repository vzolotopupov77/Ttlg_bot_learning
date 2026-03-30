"""Pytest fixtures for backend API tests."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient

from ttlg_backend.api.dialogue import get_llm_client
from ttlg_backend.config import get_settings
from ttlg_backend.db import ensure_sqlite_schema, init_db, reset_engine
from ttlg_backend.main import app


@pytest.fixture(autouse=True)
async def reset_global_engine() -> AsyncGenerator[None, None]:
    """Avoid leaking async engine / SQLite state between tests."""
    await reset_engine()
    yield
    await reset_engine()


@pytest.fixture(autouse=True)
def reset_cached_settings() -> Generator[None, None, None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
async def dialogue_client(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client with in-memory SQLite, schema, seeded student, mock LLM."""
    monkeypatch.setenv("TTLG_ALLOW_SQLITE_TEST", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    get_settings.cache_clear()

    settings = get_settings()
    init_db(settings)
    await ensure_sqlite_schema(settings)

    class MockLLM:
        async def complete_chat(self, *, system_prompt: str, user_message: str) -> str:
            return "Mock LLM answer"

    app.dependency_overrides[get_llm_client] = lambda: MockLLM()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_user = await ac.post(
            "/v1/users",
            json={"name": "Test Student", "role": "student", "telegram_id": 999001},
        )
        assert create_user.status_code == 201, create_user.text
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def api_client_sqlite(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[AsyncClient, None]:
    """Client with empty SQLite DB (CRUD / integration tests)."""
    monkeypatch.setenv("TTLG_ALLOW_SQLITE_TEST", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    get_settings.cache_clear()
    settings = get_settings()
    init_db(settings)
    await ensure_sqlite_schema(settings)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
