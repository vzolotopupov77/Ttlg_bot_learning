"""Pytest fixtures for backend API tests (PostgreSQL).

Isolation strategy: each test gets a clean schema via drop_all + create_all.
This guarantees full isolation without requiring session-scoped event loops,
which have known compatibility issues with asyncpg.
"""

from __future__ import annotations

import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-for-jwt-minimum-length-32chars")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ttlg_backend.api.dialogue import get_llm_client
from ttlg_backend.config import get_settings
from ttlg_backend.db import get_session
from ttlg_backend.main import app
from ttlg_backend.storage.models import Base

_DEFAULT_TEST_URL = "postgresql+asyncpg://ttlg:ttlg@127.0.0.1:5432/ttlg_test"


def _test_db_url() -> str:
    return os.environ.get("DATABASE_TEST_URL", _DEFAULT_TEST_URL)


@pytest.fixture
async def pg_session() -> AsyncGenerator[AsyncSession, None]:
    """Function-scoped session on a fresh schema (drop + create per test)."""
    engine = create_async_engine(_test_db_url(), echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def api_client_sqlite(pg_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client backed by PostgreSQL (name kept for backward compat)."""
    get_settings.cache_clear()

    async def _override() -> AsyncGenerator[AsyncSession, None]:
        yield pg_session

    app.dependency_overrides[get_session] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_session, None)
    get_settings.cache_clear()


@pytest.fixture
async def dialogue_client(pg_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """HTTP client with PostgreSQL session and mock LLM; seeds one student user."""
    get_settings.cache_clear()

    async def _override() -> AsyncGenerator[AsyncSession, None]:
        yield pg_session

    class MockLLM:
        async def complete_chat(self, *, system_prompt: str, user_message: str) -> str:
            return "Mock LLM answer"

    app.dependency_overrides[get_session] = _override
    app.dependency_overrides[get_llm_client] = lambda: MockLLM()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_user = await ac.post(
            "/v1/users",
            json={"name": "Test Student", "role": "student", "telegram_id": 999001},
        )
        assert create_user.status_code == 201, create_user.text
        yield ac

    app.dependency_overrides.pop(get_session, None)
    app.dependency_overrides.pop(get_llm_client, None)
    get_settings.cache_clear()
