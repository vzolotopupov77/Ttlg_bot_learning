"""Lesson CRUD (MVP + frontend flags / full update)."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.deps import get_current_user
from ttlg_backend.api.errors import api_error
from ttlg_backend.db import get_session
from ttlg_backend.dependencies import require_auth
from ttlg_backend.storage.models import LessonStatus, User
from ttlg_backend.storage.repositories import lessons as lessons_repo

router = APIRouter(prefix="/lessons", tags=["lessons"])


class LessonCreate(BaseModel):
    student_id: UUID = Field(..., description="UUID ученика")
    teacher_id: UUID = Field(..., description="UUID преподавателя")
    topic: str = Field(..., min_length=1, max_length=512, description="Тема занятия")
    scheduled_at: datetime = Field(..., description="Время занятия (timezone-aware предпочтителен)")
    status: LessonStatus = Field(
        default=LessonStatus.scheduled,
        description="Статус занятия",
    )
    notes: str | None = Field(default=None, description="Заметки (что принести и т.п.)")
    duration_minutes: int = Field(
        default=60,
        ge=1,
        le=32767,
        description="Длительность занятия в минутах (по умолчанию 60)",
    )


class LessonRead(BaseModel):
    id: UUID = Field(..., description="Идентификатор занятия")
    student_id: UUID = Field(..., description="UUID ученика")
    teacher_id: UUID = Field(..., description="UUID преподавателя")
    topic: str = Field(..., description="Тема")
    scheduled_at: datetime = Field(..., description="Запланированное время")
    duration_minutes: int = Field(..., description="Длительность занятия, минуты")
    status: LessonStatus = Field(..., description="Текущий статус")
    notes: str | None = Field(default=None, description="Заметки")

    model_config = {"from_attributes": True}


class LessonFlagsPatch(BaseModel):
    notification_sent: bool | None = None
    confirmed_by_student: bool | None = None
    homework_sent: bool | None = None
    solution_received: bool | None = None
    solution_checked: bool | None = None


class LessonStatusPatch(BaseModel):
    status: LessonStatus = Field(..., description="Новый статус занятия")


class LessonPutBody(BaseModel):
    student_id: UUID
    teacher_id: UUID
    topic: str = Field(..., min_length=1, max_length=512)
    scheduled_at: datetime
    status: LessonStatus
    notes: str | None = None
    duration_minutes: int = Field(default=60, ge=1, le=32767)


@router.post(
    "",
    response_model=LessonRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать занятие",
    description="Создаёт запись занятия для пары ученик–преподаватель.",
)
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
        duration_minutes=body.duration_minutes,
    )
    await session.commit()
    await session.refresh(lesson)
    return LessonRead.model_validate(lesson)


@router.get(
    "/{lesson_id}",
    response_model=LessonRead,
    summary="Получить занятие по id",
    description="Возвращает занятие или 404.",
)
async def read_lesson(
    lesson_id: UUID,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonRead | JSONResponse:
    lesson = await lessons_repo.get_lesson_by_id(session, lesson_id)
    if lesson is None:
        return api_error(404, "not_found", "Lesson not found")
    return LessonRead.model_validate(lesson)


@router.patch(
    "/{lesson_id}/status",
    response_model=LessonRead,
    summary="Обновить статус занятия",
    description="Частичное обновление: только `status`.",
)
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


@router.put(
    "/{lesson_id}",
    response_model=LessonRead,
    summary="Полностью обновить занятие",
)
async def put_lesson(
    lesson_id: UUID,
    body: LessonPutBody,
    _user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonRead | JSONResponse:
    _ = _user
    lesson = await lessons_repo.update_lesson_full(
        session,
        lesson_id,
        student_id=body.student_id,
        teacher_id=body.teacher_id,
        topic=body.topic,
        scheduled_at=body.scheduled_at,
        duration_minutes=body.duration_minutes,
        status=body.status,
        notes=body.notes,
    )
    if lesson is None:
        return api_error(404, "not_found", "Lesson not found")
    await session.commit()
    await session.refresh(lesson)
    return LessonRead.model_validate(lesson)


@router.delete(
    "/{lesson_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Удалить занятие",
)
async def delete_lesson(
    lesson_id: UUID,
    _user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Response | JSONResponse:
    _ = _user
    ok = await lessons_repo.delete_lesson(session, lesson_id)
    if not ok:
        return api_error(404, "not_found", "Lesson not found")
    await session.commit()
    return Response(status_code=204)


class LessonReadWithFlags(LessonRead):
    notification_sent: bool
    confirmed_by_student: bool
    homework_sent: bool
    solution_received: bool
    solution_checked: bool

    model_config = {"from_attributes": True}


@router.patch(
    "/{lesson_id}/flags",
    response_model=LessonReadWithFlags,
    summary="Обновить флаги занятия",
)
async def patch_lesson_flags(
    lesson_id: UUID,
    body: LessonFlagsPatch,
    _user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonReadWithFlags | JSONResponse:
    _ = _user
    lesson = await lessons_repo.update_lesson_flags(
        session,
        lesson_id,
        notification_sent=body.notification_sent,
        confirmed_by_student=body.confirmed_by_student,
        homework_sent=body.homework_sent,
        solution_received=body.solution_received,
        solution_checked=body.solution_checked,
    )
    if lesson is None:
        return api_error(404, "not_found", "Lesson not found")
    await session.commit()
    await session.refresh(lesson)
    return LessonReadWithFlags.model_validate(lesson)
