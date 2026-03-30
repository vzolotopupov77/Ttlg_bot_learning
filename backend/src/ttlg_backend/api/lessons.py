"""Lesson CRUD (MVP)."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.errors import api_error
from ttlg_backend.db import get_session
from ttlg_backend.dependencies import require_auth
from ttlg_backend.storage.models import LessonStatus
from ttlg_backend.storage.repositories import lessons as lessons_repo

router = APIRouter(prefix="/lessons", tags=["lessons"])


class LessonCreate(BaseModel):
    student_id: UUID
    teacher_id: UUID
    topic: str = Field(..., min_length=1, max_length=512)
    scheduled_at: datetime
    status: LessonStatus = LessonStatus.scheduled
    notes: str | None = None


class LessonRead(BaseModel):
    id: UUID
    student_id: UUID
    teacher_id: UUID
    topic: str
    scheduled_at: datetime
    status: LessonStatus
    notes: str | None

    model_config = {"from_attributes": True}


class LessonStatusPatch(BaseModel):
    status: LessonStatus


@router.post("", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    body: LessonCreate,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonRead:
    lesson = await lessons_repo.create_lesson(
        session,
        student_id=body.student_id,
        teacher_id=body.teacher_id,
        topic=body.topic,
        scheduled_at=body.scheduled_at,
        status=body.status,
        notes=body.notes,
    )
    await session.commit()
    await session.refresh(lesson)
    return LessonRead.model_validate(lesson)


@router.get("/{lesson_id}", response_model=LessonRead)
async def read_lesson(
    lesson_id: UUID,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonRead | JSONResponse:
    lesson = await lessons_repo.get_lesson_by_id(session, lesson_id)
    if lesson is None:
        return api_error(404, "not_found", "Lesson not found")
    return LessonRead.model_validate(lesson)


@router.patch("/{lesson_id}/status", response_model=LessonRead)
async def patch_lesson_status(
    lesson_id: UUID,
    body: LessonStatusPatch,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonRead | JSONResponse:
    lesson = await lessons_repo.update_lesson_status(session, lesson_id, body.status)
    if lesson is None:
        return api_error(404, "not_found", "Lesson not found")
    await session.commit()
    await session.refresh(lesson)
    return LessonRead.model_validate(lesson)
