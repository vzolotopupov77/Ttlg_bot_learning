"""Smoke tests for GET /health."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from ttlg_backend.config import get_settings
from ttlg_backend.main import app


async def test_health_without_database_returns_503(monkeypatch: pytest.MonkeyPatch) -> None:
    # Пустая строка → None через empty_database_url_as_none; перекрывает значение из .env-файла.
    monkeypatch.setenv("DATABASE_URL", "")
    monkeypatch.setenv("TTLG_ALLOW_SQLITE_TEST", "0")
    get_settings.cache_clear()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["database"] == "not_configured"
