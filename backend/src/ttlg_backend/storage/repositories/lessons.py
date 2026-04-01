"""Lesson persistence helpers."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import Lesson, LessonStatus


async def create_lesson(
    session: AsyncSession,
    *,
    student_id: UUID,
    teacher_id: UUID,
    topic: str,
    scheduled_at: datetime,
    status: LessonStatus = LessonStatus.scheduled,
    notes: str | None = None,
) -> Lesson:
    lesson = Lesson(
        student_id=student_id,
        teacher_id=teacher_id,
        topic=topic,
        scheduled_at=scheduled_at,
        status=status,
        notes=notes,
    )
    session.add(lesson)
    await session.flush()
    return lesson


async def get_lesson_by_id(session: AsyncSession, lesson_id: UUID) -> Lesson | None:
    return await session.get(Lesson, lesson_id)


async def update_lesson_status(
    session: AsyncSession,
    lesson_id: UUID,
    status: LessonStatus,
) -> Lesson | None:
    lesson = await session.get(Lesson, lesson_id)
    if lesson is None:
        return None
    lesson.status = status
    await session.flush()
    return lesson


async def list_recent_lessons_for_student(
    session: AsyncSession,
    student_id: UUID,
    *,
    limit: int = 8,
) -> list[Lesson]:
    stmt = select(Lesson).where(Lesson.student_id == student_id).order_by(Lesson.scheduled_at.desc()).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())
