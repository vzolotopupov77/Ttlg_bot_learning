"""POST /v1/dialogue/message — persisted dialogue + LLM."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.errors import api_error
from ttlg_backend.config import get_settings
from ttlg_backend.db import get_session
from ttlg_backend.llm.client import LLMClient
from ttlg_backend.llm.errors import LLMUnavailableError
from ttlg_backend.services import dialogue_service as dialogue_svc

logger = logging.getLogger(__name__)

router = APIRouter(tags=["dialogue"])


class DialogueMessageRequest(BaseModel):
    telegram_id: int = Field(..., description="Telegram ID ученика (целое число)")
    text: str = Field(..., description="Текст сообщения ученика; после trim не пустой")
    dialogue_id: UUID | None = Field(
        default=None,
        description="Продолжить существующий диалог; если не задан — создаётся новый",
    )

    @field_validator("text")
    @classmethod
    def text_non_empty_after_strip(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("text must not be empty")
        return s


class DialogueMessageResponse(BaseModel):
    """Ответ ассистента после обработки сообщения ученика."""

    dialogue_id: str = Field(..., description="Идентификатор диалога (UUID строкой)")
    message_id: str = Field(..., description="Идентификатор сообщения ассистента (UUID строкой)")
    text: str = Field(..., description="Текст ответа ассистента")
    created_at: str = Field(
        ...,
        description="Время создания ответа, ISO 8601 в UTC (суффикс Z)",
    )


def get_llm_client() -> LLMClient:
    return LLMClient.from_settings(get_settings())


def _format_created_at(dt: datetime) -> str:
    utc = dt.astimezone(UTC).replace(microsecond=0)
    return utc.isoformat().replace("+00:00", "Z")


@router.post(
    "/dialogue/message",
    response_model=DialogueMessageResponse,
    summary="Сообщение в диалог с ассистентом",
    description=(
        "Сохраняет реплику ученика и ответ ассистента в БД; при наличии данных подмешивает контекст занятий и ДЗ. "
        "Пользователь с указанным `telegram_id` должен быть заранее создан через `POST /v1/users`."
    ),
)
async def post_dialogue_message(
    body: DialogueMessageRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    llm: Annotated[LLMClient, Depends(get_llm_client)],
) -> DialogueMessageResponse | JSONResponse:
    try:
        result = await dialogue_svc.process_dialogue_message(
            session,
            llm,
            telegram_id=body.telegram_id,
            text=body.text,
            dialogue_id=body.dialogue_id,
        )
    except dialogue_svc.UserNotFound:
        return api_error(404, "user_not_found", "User with given telegram_id was not found")
    except dialogue_svc.DialogueNotFound:
        return api_error(404, "dialogue_not_found", "Dialogue was not found")
    except LLMUnavailableError:
        return api_error(503, "llm_unavailable", "The assistant is temporarily unavailable")
    except Exception:  # noqa: BLE001
        logger.exception("Unexpected error in dialogue endpoint")
        return api_error(500, "internal_error", "Internal server error")

    return DialogueMessageResponse(
        dialogue_id=str(result.dialogue_id),
        message_id=str(result.assistant_message_id),
        text=result.text,
        created_at=_format_created_at(result.created_at),
    )
