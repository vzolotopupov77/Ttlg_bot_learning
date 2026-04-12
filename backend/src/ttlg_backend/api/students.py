"""Students CRUD (teacher) and nested resources."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.deps import require_teacher
from ttlg_backend.api.errors import api_error
from ttlg_backend.db import get_session
from ttlg_backend.storage.models import User, UserRole
from ttlg_backend.storage.repositories import dialogues as dialogues_repo
from ttlg_backend.storage.repositories import lessons as lessons_repo
from ttlg_backend.storage.repositories import progress_summary
from ttlg_backend.storage.repositories import users as users_repo

router = APIRouter(prefix="/students", tags=["students"])


class StudentCreateBody(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    class_label: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    notes: str | None = None

    @field_validator("class_label", "phone", "notes", mode="before")
    @classmethod
    def strip_opt(cls, v: object) -> str | None:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            return s if s else None
        return str(v)


class StudentUpdateBody(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    class_label: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    notes: str | None = None

    @field_validator("class_label", "phone", "notes", mode="before")
    @classmethod
    def strip_opt(cls, v: object) -> str | None:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            return s if s else None
        return str(v)


class StudentRead(BaseModel):
    id: str
    name: str
    role: str
    class_label: str | None
    phone: str | None
    email: str | None
    notes: str | None
    created_at: datetime


class PaginatedStudents(BaseModel):
    items: list[StudentRead]
    total: int
    limit: int
    offset: int


class LessonItemOut(BaseModel):
    id: str
    student_id: str
    teacher_id: str
    topic: str
    scheduled_at: datetime
    duration_minutes: int
    status: str
    notes: str | None

    model_config = {"from_attributes": True}


class PaginatedLessons(BaseModel):
    items: list[LessonItemOut]
    total: int
    limit: int
    offset: int


class DialogueMessageOut(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime


class DialogueFeedResponse(BaseModel):
    items: list[DialogueMessageOut]
    total: int
    limit: int
    offset: int


class StatsRead(BaseModel):
    student_id: str
    lessons_completed: int
    lessons_total: int
    assignments_done: int
    assignments_total: int


@router.get("", response_model=PaginatedStudents)
async def list_students(
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PaginatedStudents:
    users, total = await users_repo.list_students(session, limit=limit, offset=offset)
    items = [
        StudentRead(
            id=str(u.id),
            name=u.name,
            role=u.role.value,
            class_label=u.class_label,
            phone=u.phone,
            email=u.email,
            notes=u.notes,
            created_at=u.created_at,
        )
        for u in users
    ]
    return PaginatedStudents(items=items, total=total, limit=limit, offset=offset)


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    body: StudentCreateBody,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> StudentRead | JSONResponse:
    if body.email:
        existing = await users_repo.get_user_by_email(session, email=str(body.email))
        if existing is not None:
            return api_error(409, "conflict", "Email already in use")
    user = await users_repo.create_user(
        session,
        name=body.name,
        role=UserRole.student,
        class_label=body.class_label,
        phone=body.phone,
        email=str(body.email) if body.email else None,
        notes=body.notes,
    )
    await session.commit()
    await session.refresh(user)
    return StudentRead(
        id=str(user.id),
        name=user.name,
        role=user.role.value,
        class_label=user.class_label,
        phone=user.phone,
        email=user.email,
        notes=user.notes,
        created_at=user.created_at,
    )


@router.get("/{student_id}", response_model=StudentRead)
async def get_student(
    student_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> StudentRead | JSONResponse:
    user = await users_repo.get_user_by_id(session, student_id)
    if user is None or user.role != UserRole.student:
        return api_error(404, "not_found", "Student not found")
    return StudentRead(
        id=str(user.id),
        name=user.name,
        role=user.role.value,
        class_label=user.class_label,
        phone=user.phone,
        email=user.email,
        notes=user.notes,
        created_at=user.created_at,
    )


@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: UUID,
    body: StudentUpdateBody,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> StudentRead | JSONResponse:
    user = await users_repo.get_user_by_id(session, student_id)
    if user is None or user.role != UserRole.student:
        return api_error(404, "not_found", "Student not found")
    if body.email:
        other = await users_repo.get_user_by_email(session, email=str(body.email))
        if other is not None and other.id != user.id:
            return api_error(409, "conflict", "Email already in use")
    await users_repo.update_user_fields(
        session,
        user,
        name=body.name,
        class_label=body.class_label,
        phone=body.phone,
        email=str(body.email) if body.email else None,
        notes=body.notes,
    )
    await session.commit()
    await session.refresh(user)
    return StudentRead(
        id=str(user.id),
        name=user.name,
        role=user.role.value,
        class_label=user.class_label,
        phone=user.phone,
        email=user.email,
        notes=user.notes,
        created_at=user.created_at,
    )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_student(
    student_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> Response | JSONResponse:
    user = await users_repo.get_user_by_id(session, student_id)
    if user is None or user.role != UserRole.student:
        return api_error(404, "not_found", "Student not found")
    await users_repo.delete_user(session, student_id)
    await session.commit()
    return Response(status_code=204)


@router.get("/{student_id}/lessons", response_model=PaginatedLessons)
async def list_student_lessons(
    student_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> PaginatedLessons | JSONResponse:
    user = await users_repo.get_user_by_id(session, student_id)
    if user is None or user.role != UserRole.student:
        return api_error(404, "not_found", "Student not found")
    lessons, total = await lessons_repo.list_lessons_for_student(
        session,
        student_id,
        limit=limit,
        offset=offset,
    )
    items = [
        LessonItemOut(
            id=str(lesson.id),
            student_id=str(lesson.student_id),
            teacher_id=str(lesson.teacher_id),
            topic=lesson.topic,
            scheduled_at=lesson.scheduled_at,
            duration_minutes=int(lesson.duration_minutes),
            status=lesson.status.value,
            notes=lesson.notes,
        )
        for lesson in lessons
    ]
    return PaginatedLessons(items=items, total=total, limit=limit, offset=offset)


@router.get("/{student_id}/dialogue", response_model=DialogueFeedResponse)
async def student_dialogue(
    student_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> DialogueFeedResponse | JSONResponse:
    user = await users_repo.get_user_by_id(session, student_id)
    if user is None or user.role != UserRole.student:
        return api_error(404, "not_found", "Student not found")
    messages, total = await dialogues_repo.list_messages_for_student(
        session,
        student_id,
        limit=limit,
        offset=offset,
    )
    items = [
        DialogueMessageOut(
            id=str(m.id),
            role=m.role.value,
            content=m.content,
            created_at=m.created_at,
        )
        for m in messages
    ]
    return DialogueFeedResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{student_id}/stats", response_model=StatsRead)
async def student_stats(
    student_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
    _teacher: Annotated[User, Depends(require_teacher)],
) -> StatsRead | JSONResponse:
    user = await users_repo.get_user_by_id(session, student_id)
    if user is None or user.role != UserRole.student:
        return api_error(404, "not_found", "Student not found")
    summary = await progress_summary.get_student_progress_summary(session, student_id)
    return StatsRead(
        student_id=summary["student_id"],
        lessons_completed=summary["lessons_completed"],
        lessons_total=summary["lessons_total"],
        assignments_done=summary["assignments_done"],
        assignments_total=summary["assignments_total"],
    )
