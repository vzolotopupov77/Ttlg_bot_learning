"""Contract smoke tests for POST /v1/dialogue/message (persisted + mock LLM)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


async def test_dialogue_success(dialogue_client: AsyncClient) -> None:
    """Happy path: valid user + non-empty text → assistant reply with all contract fields."""
    response = await dialogue_client.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999001, "text": "Hello"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "dialogue_id" in data
    assert "message_id" in data
    assert data["text"] == "Mock LLM answer"
    assert "created_at" in data


async def test_dialogue_continue_with_dialogue_id(dialogue_client: AsyncClient) -> None:
    """Continuation: second message with existing dialogue_id keeps same dialogue."""
    first = await dialogue_client.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999001, "text": "First message"},
    )
    assert first.status_code == 200
    dialogue_id = first.json()["dialogue_id"]

    second = await dialogue_client.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999001, "text": "Follow-up", "dialogue_id": dialogue_id},
    )
    assert second.status_code == 200
    assert second.json()["dialogue_id"] == dialogue_id


async def test_dialogue_empty_text_returns_422(dialogue_client: AsyncClient) -> None:
    """Whitespace-only text fails validation before any business logic."""
    response = await dialogue_client.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999001, "text": "   "},
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


async def test_dialogue_unknown_user_returns_404(dialogue_client: AsyncClient) -> None:
    """telegram_id not in allowed list → user_not_found."""
    response = await dialogue_client.post(
        "/v1/dialogue/message",
        json={"telegram_id": 999002, "text": "Hi"},
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "user_not_found"


@pytest.mark.parametrize(
    ("payload", "expected_status"),
    [
        ({"text": "no telegram_id"}, 422),
        ({"telegram_id": 999001}, 422),
        ({}, 422),
    ],
    ids=["missing_telegram_id", "missing_text", "empty_body"],
)
async def test_dialogue_missing_required_fields(
    dialogue_client: AsyncClient,
    payload: dict,
    expected_status: int,
) -> None:
    """Missing required fields all yield 422 validation_error."""
    response = await dialogue_client.post("/v1/dialogue/message", json=payload)
    assert response.status_code == expected_status
    assert response.json()["error"]["code"] == "validation_error"
