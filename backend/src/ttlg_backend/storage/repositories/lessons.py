"""Lesson persistence helpers."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ttlg_backend.storage.models import Lesson, LessonStatus


def _week_bounds(week_start: date) -> tuple[datetime, datetime]:
    start = datetime(week_start.year, week_start.month, week_start.day, tzinfo=UTC)
    end = start + timedelta(days=7)
    return start, end


async def list_weekly_lessons_for_student(
    session: AsyncSession,
    *,
    student_id: UUID,
    week_start: date,
) -> list[Lesson]:
    start, end = _week_bounds(week_start)
    stmt = (
        select(Lesson)
        .where(
            Lesson.student_id == student_id,
            Lesson.scheduled_at >= start,
            Lesson.scheduled_at < end,
        )
        .options(joinedload(Lesson.teacher))
        .order_by(Lesson.scheduled_at.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().unique().all())


async def create_lesson(
    session: AsyncSession,
    *,
    student_id: UUID,
    teacher_id: UUID,
    topic: str,
    scheduled_at: datetime,
    status: LessonStatus = LessonStatus.scheduled,
    notes: str | None = None,
    duration_minutes: int = 60,
) -> Lesson:
    lesson = Lesson(
        student_id=student_id,
        teacher_id=teacher_id,
        topic=topic,
        scheduled_at=scheduled_at,
        status=status,
        notes=notes,
        duration_minutes=duration_minutes,
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


async def list_lessons_for_student(
    session: AsyncSession,
    student_id: UUID,
    *,
    limit: int,
    offset: int,
) -> tuple[list[Lesson], int]:
    count_stmt = select(func.count()).select_from(Lesson).where(Lesson.student_id == student_id)
    total = int((await session.execute(count_stmt)).scalar_one())
    stmt = (
        select(Lesson)
        .where(Lesson.student_id == student_id)
        .order_by(Lesson.scheduled_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all()), total


async def delete_lesson(session: AsyncSession, lesson_id: UUID) -> bool:
    lesson = await session.get(Lesson, lesson_id)
    if lesson is None:
        return False
    await session.delete(lesson)
    await session.flush()
    return True


async def update_lesson_full(
    session: AsyncSession,
    lesson_id: UUID,
    *,
    student_id: UUID,
    teacher_id: UUID,
    topic: str,
    scheduled_at: datetime,
    duration_minutes: int,
    status: LessonStatus,
    notes: str | None,
) -> Lesson | None:
    lesson = await session.get(Lesson, lesson_id)
    if lesson is None:
        return None
    lesson.student_id = student_id
    lesson.teacher_id = teacher_id
    lesson.topic = topic
    lesson.scheduled_at = scheduled_at
    lesson.duration_minutes = duration_minutes
    lesson.status = status
    lesson.notes = notes
    await session.flush()
    return lesson


async def update_lesson_flags(
    session: AsyncSession,
    lesson_id: UUID,
    *,
    notification_sent: bool | None = None,
    confirmed_by_student: bool | None = None,
    homework_sent: bool | None = None,
    solution_received: bool | None = None,
    solution_checked: bool | None = None,
) -> Lesson | None:
    lesson = await session.get(Lesson, lesson_id)
    if lesson is None:
        return None
    if notification_sent is not None:
        lesson.notification_sent = notification_sent
    if confirmed_by_student is not None:
        lesson.confirmed_by_student = confirmed_by_student
    if homework_sent is not None:
        lesson.homework_sent = homework_sent
    if solution_received is not None:
        lesson.solution_received = solution_received
    if solution_checked is not None:
        lesson.solution_checked = solution_checked
    await session.flush()
    return lesson
