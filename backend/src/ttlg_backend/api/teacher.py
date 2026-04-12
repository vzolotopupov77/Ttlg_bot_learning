"""Teacher dashboard endpoints."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.deps import require_teacher
from ttlg_backend.api.errors import api_error
from ttlg_backend.db import get_session
from ttlg_backend.storage.models import Lesson, User
from ttlg_backend.storage.repositories import teacher_repo

router = APIRouter(prefix="/teacher", tags=["teacher"])


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


class BotRequestItem(BaseModel):
    message_id: str
    dialogue_id: str
    student_id: str
    student_name: str
    text: str
    created_at: datetime


class BotRequestsResponse(BaseModel):
    items: list[BotRequestItem]
    total: int
    limit: int
    offset: int


class UnconfirmedResponse(BaseModel):
    items: list[ScheduleLessonItem]
    total: int
    limit: int
    offset: int


class RemindResponse(BaseModel):
    notified_count: int


class RescheduleItemOut(BaseModel):
    id: str
    lesson_id: str
    student_id: str
    student_name: str
    proposed_time: datetime
    requested_at: datetime
    status: str


class RescheduleListResponse(BaseModel):
    items: list[RescheduleItemOut]
    total: int
    limit: int
    offset: int


class ReschedulePatchBody(BaseModel):
    status: str = Field(..., pattern="^(accepted|rejected)$")


def _lesson_to_item(lesson: Lesson) -> ScheduleLessonItem:
    student = lesson.student
    assert student is not None
    ends = lesson.scheduled_at + timedelta(minutes=int(lesson.duration_minutes))
    return ScheduleLessonItem(
        id=str(lesson.id),
        student_id=str(lesson.student_id),
        student_name=student.name,
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
async def teacher_schedule(
    week_start: Annotated[date, Query(description="Monday of week (YYYY-MM-DD)")],
    session: Annotated[AsyncSession, Depends(get_session)],
    teacher: Annotated[User, Depends(require_teacher)],
) -> ScheduleResponse:
    lessons = await teacher_repo.list_weekly_lessons(
        session,
        teacher_id=teacher.id,
        week_start=week_start,
    )
    return ScheduleResponse(
        week_start=week_start,
        items=[_lesson_to_item(lesson) for lesson in lessons],
    )


@router.get("/bot-requests", response_model=BotRequestsResponse)
async def bot_requests(
    session: Annotated[AsyncSession, Depends(get_session)],
    teacher: Annotated[User, Depends(require_teacher)],
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> BotRequestsResponse:
    _ = teacher
    rows, total = await teacher_repo.list_recent_user_messages(session, limit=limit, offset=offset)
    items = [
        BotRequestItem(
            message_id=str(m.id),
            dialogue_id=str(d.id),
            student_id=str(u.id),
            student_name=u.name,
            text=m.content,
            created_at=m.created_at,
        )
        for m, d, u in rows
    ]
    return BotRequestsResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/unconfirmed-lessons", response_model=UnconfirmedResponse)
async def unconfirmed_lessons(
    session: Annotated[AsyncSession, Depends(get_session)],
    teacher: Annotated[User, Depends(require_teacher)],
    days: Annotated[int, Query(ge=1, le=30)] = 2,
) -> UnconfirmedResponse:
    lessons = await teacher_repo.list_unconfirmed_lessons(
        session,
        teacher_id=teacher.id,
        days=days,
    )
    items = [_lesson_to_item(lesson) for lesson in lessons]
    return UnconfirmedResponse(items=items, total=len(items), limit=len(items), offset=0)


@router.get("/pending-homework", response_model=UnconfirmedResponse)
async def pending_homework(
    session: Annotated[AsyncSession, Depends(get_session)],
    teacher: Annotated[User, Depends(require_teacher)],
    days: Annotated[int, Query(ge=1, le=30)] = 2,
) -> UnconfirmedResponse:
    lessons = await teacher_repo.list_pending_homework_lessons(
        session,
        teacher_id=teacher.id,
        days=days,
    )
    items = [_lesson_to_item(lesson) for lesson in lessons]
    return UnconfirmedResponse(items=items, total=len(items), limit=len(items), offset=0)


@router.post("/remind-unconfirmed", response_model=RemindResponse)
async def remind_unconfirmed(
    teacher: Annotated[User, Depends(require_teacher)],
) -> RemindResponse:
    _ = teacher
    return RemindResponse(notified_count=0)


@router.post("/remind-pending-homework", response_model=RemindResponse)
async def remind_pending_homework(
    teacher: Annotated[User, Depends(require_teacher)],
) -> RemindResponse:
    _ = teacher
    return RemindResponse(notified_count=0)


@router.get("/reschedule-requests", response_model=RescheduleListResponse)
async def list_reschedule_requests(
    session: Annotated[AsyncSession, Depends(get_session)],
    teacher: Annotated[User, Depends(require_teacher)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> RescheduleListResponse:
    rows = await teacher_repo.list_reschedule_requests_for_teacher(session, teacher_id=teacher.id)
    total = len(rows)
    page = rows[offset : offset + limit]
    items = [
        RescheduleItemOut(
            id=str(r.id),
            lesson_id=str(r.lesson_id),
            student_id=str(r.student_id),
            student_name=r.student.name,
            proposed_time=r.proposed_time,
            requested_at=r.requested_at,
            status=r.status,
        )
        for r in page
    ]
    return RescheduleListResponse(items=items, total=total, limit=limit, offset=offset)


@router.patch("/reschedule-requests/{request_id}", response_model=RescheduleItemOut)
async def patch_reschedule_request(
    request_id: UUID,
    body: ReschedulePatchBody,
    session: Annotated[AsyncSession, Depends(get_session)],
    teacher: Annotated[User, Depends(require_teacher)],
) -> RescheduleItemOut | JSONResponse:
    req = await teacher_repo.get_reschedule_request_for_teacher(
        session,
        request_id=request_id,
        teacher_id=teacher.id,
    )
    if req is None:
        return api_error(404, "not_found", "Reschedule request not found")
    if req.status != "pending":
        return api_error(409, "conflict", "Request already processed")
    req.status = body.status
    await session.commit()
    await session.refresh(req)
    return RescheduleItemOut(
        id=str(req.id),
        lesson_id=str(req.lesson_id),
        student_id=str(req.student_id),
        student_name=req.student.name,
        proposed_time=req.proposed_time,
        requested_at=req.requested_at,
        status=req.status,
    )
