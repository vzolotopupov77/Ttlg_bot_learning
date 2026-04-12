"""Teacher dashboard queries."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ttlg_backend.storage.models import (
    Dialogue,
    Lesson,
    LessonStatus,
    Message,
    MessageRole,
    RescheduleRequest,
    User,
)


def _week_bounds(week_start: date) -> tuple[datetime, datetime]:
    start = datetime(week_start.year, week_start.month, week_start.day, tzinfo=UTC)
    end = start + timedelta(days=7)
    return start, end


async def list_weekly_lessons(
    session: AsyncSession,
    *,
    teacher_id: UUID,
    week_start: date,
) -> list[Lesson]:
    start, end = _week_bounds(week_start)
    stmt = (
        select(Lesson)
        .where(
            Lesson.teacher_id == teacher_id,
            Lesson.scheduled_at >= start,
            Lesson.scheduled_at < end,
        )
        .options(joinedload(Lesson.student))
        .order_by(Lesson.scheduled_at.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().unique().all())


async def list_recent_user_messages(
    session: AsyncSession,
    *,
    limit: int,
    offset: int,
) -> tuple[list[tuple[Message, Dialogue, User]], int]:
    base = (
        select(Message, Dialogue, User)
        .join(Dialogue, Message.dialogue_id == Dialogue.id)
        .join(User, Dialogue.student_id == User.id)
        .where(Message.role == MessageRole.user)
    )
    count_stmt = (
        select(func.count())
        .select_from(Message)
        .join(Dialogue, Message.dialogue_id == Dialogue.id)
        .where(Message.role == MessageRole.user)
    )
    total = int((await session.execute(count_stmt)).scalar_one())
    stmt = base.order_by(Message.created_at.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    return list(result.all()), total


async def list_unconfirmed_lessons(
    session: AsyncSession,
    *,
    teacher_id: UUID,
    days: int,
) -> list[Lesson]:
    now = datetime.now(tz=UTC)
    until = now + timedelta(days=days)
    stmt = (
        select(Lesson)
        .where(
            Lesson.teacher_id == teacher_id,
            Lesson.scheduled_at >= now,
            Lesson.scheduled_at <= until,
            Lesson.confirmed_by_student.is_(False),
            Lesson.status == LessonStatus.scheduled,
        )
        .options(joinedload(Lesson.student))
        .order_by(Lesson.scheduled_at.asc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().unique().all())


async def list_pending_homework_lessons(
    session: AsyncSession,
    *,
    teacher_id: UUID,
    days: int,
) -> list[Lesson]:
    now = datetime.now(tz=UTC)
    since = now - timedelta(days=days)
    stmt = (
        select(Lesson)
        .where(
            Lesson.teacher_id == teacher_id,
            Lesson.scheduled_at >= since,
            Lesson.scheduled_at <= now,
            Lesson.homework_sent.is_(True),
            Lesson.solution_received.is_(False),
        )
        .options(joinedload(Lesson.student))
        .order_by(Lesson.scheduled_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().unique().all())


async def list_reschedule_requests_for_teacher(
    session: AsyncSession,
    *,
    teacher_id: UUID,
) -> list[RescheduleRequest]:
    stmt = (
        select(RescheduleRequest)
        .join(Lesson, RescheduleRequest.lesson_id == Lesson.id)
        .where(Lesson.teacher_id == teacher_id)
        .options(joinedload(RescheduleRequest.lesson), joinedload(RescheduleRequest.student))
        .order_by(RescheduleRequest.requested_at.desc())
    )
    result = await session.execute(stmt)
    return list(result.scalars().unique().all())


async def get_reschedule_request_for_teacher(
    session: AsyncSession,
    *,
    request_id: UUID,
    teacher_id: UUID,
) -> RescheduleRequest | None:
    stmt = (
        select(RescheduleRequest)
        .join(Lesson, RescheduleRequest.lesson_id == Lesson.id)
        .where(RescheduleRequest.id == request_id, Lesson.teacher_id == teacher_id)
        .options(joinedload(RescheduleRequest.lesson), joinedload(RescheduleRequest.student))
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
