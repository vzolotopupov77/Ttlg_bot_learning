"""Student: own schedule."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.deps import require_student
from ttlg_backend.db import get_session
from ttlg_backend.storage.models import Lesson, User
from ttlg_backend.storage.repositories import lessons as lessons_repo

router = APIRouter(prefix="/student", tags=["student"])


class LessonFlagsOut(BaseModel):
    notification_sent: bool
    confirmed_by_student: bool
    homework_sent: bool
    solution_received: bool
    solution_checked: bool


class ScheduleLessonItem(BaseModel):
    id: str
    student_id: str
    student_name: str
    topic: str
    scheduled_at: datetime
    ends_at: datetime
    duration_minutes: int
    status: str
    flags: LessonFlagsOut


class ScheduleResponse(BaseModel):
    week_start: date
    items: list[ScheduleLessonItem]


def _item(lesson: Lesson, *, student_name: str) -> ScheduleLessonItem:
    ends = lesson.scheduled_at + timedelta(minutes=int(lesson.duration_minutes))
    return ScheduleLessonItem(
        id=str(lesson.id),
        student_id=str(lesson.student_id),
        student_name=student_name,
        topic=lesson.topic,
        scheduled_at=lesson.scheduled_at,
        ends_at=ends,
        duration_minutes=int(lesson.duration_minutes),
        status=lesson.status.value,
        flags=LessonFlagsOut(
            notification_sent=lesson.notification_sent,
            confirmed_by_student=lesson.confirmed_by_student,
            homework_sent=lesson.homework_sent,
            solution_received=lesson.solution_received,
            solution_checked=lesson.solution_checked,
        ),
    )


@router.get("/schedule", response_model=ScheduleResponse)
async def student_schedule(
    week_start: Annotated[date, Query(description="Monday of week (YYYY-MM-DD)")],
    session: Annotated[AsyncSession, Depends(get_session)],
    user: Annotated[User, Depends(require_student)],
) -> ScheduleResponse:
    lessons = await lessons_repo.list_weekly_lessons_for_student(
        session,
        student_id=user.id,
        week_start=week_start,
    )
    return ScheduleResponse(
        week_start=week_start,
        items=[_item(lesson, student_name=user.name) for lesson in lessons],
    )
