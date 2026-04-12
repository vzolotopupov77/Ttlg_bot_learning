"""System settings (teacher)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.deps import require_teacher
from ttlg_backend.db import get_session
from ttlg_backend.storage.models import User
from ttlg_backend.storage.repositories import settings_repo

router = APIRouter(prefix="/settings", tags=["settings"])

KEY_TEACHER_NAME = "teacher_name"
KEY_DEFAULT_DURATION = "default_lesson_duration_minutes"
KEY_LESSON_REMINDER = "lesson_reminder_hours_before"
KEY_HW_REMINDER = "homework_reminder_hours_before"


class SettingsBody(BaseModel):
    teacher_name: str = Field(..., min_length=1)
    default_lesson_duration_minutes: int = Field(..., ge=15, le=240)
    lesson_reminder_hours_before: int = Field(..., ge=1, le=168)
    homework_reminder_hours_before: int = Field(..., ge=1, le=336)


def _merge_defaults(raw: dict[str, str]) -> SettingsBody:
    return SettingsBody(
        teacher_name=raw.get(KEY_TEACHER_NAME, "Teacher"),
        default_lesson_duration_minutes=int(raw.get(KEY_DEFAULT_DURATION, "60")),
        lesson_reminder_hours_before=int(raw.get(KEY_LESSON_REMINDER, "24")),
        homework_reminder_hours_before=int(raw.get(KEY_HW_REMINDER, "48")),
    )


@router.get("", response_model=SettingsBody)
async def get_settings(
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> SettingsBody:
    raw = await settings_repo.get_all(session)
    return _merge_defaults(raw)


@router.put("", response_model=SettingsBody)
async def put_settings(
    body: SettingsBody,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> SettingsBody:
    await settings_repo.upsert_many(
        session,
        {
            KEY_TEACHER_NAME: body.teacher_name,
            KEY_DEFAULT_DURATION: str(body.default_lesson_duration_minutes),
            KEY_LESSON_REMINDER: str(body.lesson_reminder_hours_before),
            KEY_HW_REMINDER: str(body.homework_reminder_hours_before),
        },
    )
    await session.commit()
    return body
