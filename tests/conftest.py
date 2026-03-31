"""Shared fixtures for bot integration tests against real backend (in-memory SQLite)."""

from __future__ import annotations

from collections.abc import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient

from ttlg_backend.api.dialogue import get_llm_client
from ttlg_backend.config import get_settings
from ttlg_backend.db import ensure_sqlite_schema, init_db, reset_engine
from ttlg_backend.main import app
from ttlg_bot.services.backend_client import BackendClient

TELEGRAM_ID_KNOWN = 100_001
TELEGRAM_ID_UNKNOWN = 999_999


@pytest.fixture(autouse=True)
async def reset_global_engine() -> AsyncGenerator[None, None]:
    await reset_engine()
    yield
    await reset_engine()


@pytest.fixture(autouse=True)
def reset_cached_settings() -> Generator[None, None, None]:
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class _MockLLM:
    async def complete_chat(self, *, system_prompt: str, user_message: str) -> str:
        return "Мок-ответ ассистента"


class _BrokenLLM:
    async def complete_chat(self, **_kwargs: object) -> str:
        from ttlg_backend.llm.errors import LLMUnavailableError

        raise LLMUnavailableError("test")


@pytest.fixture
async def backend_app(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[None, None]:
    """Инициализация backend с SQLite + Mock LLM."""
    monkeypatch.setenv("TTLG_ALLOW_SQLITE_TEST", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    get_settings.cache_clear()

    settings = get_settings()
    init_db(settings)
    await ensure_sqlite_schema(settings)
    app.dependency_overrides[get_llm_client] = lambda: _MockLLM()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def backend_app_llm_broken(monkeypatch: pytest.MonkeyPatch) -> AsyncGenerator[None, None]:
    """Инициализация backend с SQLite + LLM, который всегда падает."""
    monkeypatch.setenv("TTLG_ALLOW_SQLITE_TEST", "1")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    get_settings.cache_clear()

    settings = get_settings()
    init_db(settings)
    await ensure_sqlite_schema(settings)
    app.dependency_overrides[get_llm_client] = lambda: _BrokenLLM()
    yield
    app.dependency_overrides.clear()


def make_bot_client(base_url: str = "http://test") -> BackendClient:
    """BackendClient, подключённый к in-process backend через ASGITransport."""
    transport = ASGITransport(app=app)
    http = AsyncClient(transport=transport, base_url=base_url)
    return BackendClient(base_url=base_url, timeout=5.0, _client=http)


async def _seed_student(client: BackendClient, telegram_id: int = TELEGRAM_ID_KNOWN) -> None:
    """Создать студента через HTTP API backend."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post(
            "/v1/users",
            json={"name": "Тест Студент", "role": "student", "telegram_id": telegram_id},
        )
        assert r.status_code == 201, r.text
