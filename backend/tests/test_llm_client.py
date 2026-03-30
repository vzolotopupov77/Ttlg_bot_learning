"""Unit tests for LLM client (HTTP mocked)."""

from __future__ import annotations

import logging

import httpx
import pytest
import respx

from ttlg_backend.config import Settings
from ttlg_backend.llm.client import LLMClient
from ttlg_backend.llm.errors import LLMUnavailableError


def _llm_settings() -> Settings:
    return Settings(
        database_url=None,
        openrouter_base_url="https://openrouter.test/v1",
        openrouter_api_key="sk-test",
        llm_model="test/model",
        llm_timeout_seconds=5.0,
        allow_sqlite_test=False,
    )


async def test_llm_client_maps_api_error_to_llm_unavailable(respx_mock: respx.MockRouter) -> None:
    respx_mock.post("https://openrouter.test/v1/chat/completions").mock(
        return_value=httpx.Response(500, json={"error": "internal"}),
    )

    client = LLMClient(_llm_settings())
    with pytest.raises(LLMUnavailableError):
        await client.complete_chat(system_prompt="sys", user_message="hi")


async def test_llm_client_success(respx_mock: respx.MockRouter) -> None:
    respx_mock.post("https://openrouter.test/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "1",
                "choices": [{"message": {"role": "assistant", "content": "  Hello  "}}],
                "model": "test/model",
            },
        ),
    )
    client = LLMClient(_llm_settings())
    out = await client.complete_chat(system_prompt="sys", user_message="hi")
    assert out == "Hello"


async def test_llm_client_does_not_log_api_key(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG)
    settings = Settings(
        database_url=None,
        openrouter_base_url="https://example.com/v1",
        openrouter_api_key="super-secret-key-12345",
        llm_model="m",
        llm_timeout_seconds=1.0,
        allow_sqlite_test=False,
    )
    _ = LLMClient(settings)
    joined = " ".join(caplog.messages)
    assert "super-secret-key-12345" not in joined
