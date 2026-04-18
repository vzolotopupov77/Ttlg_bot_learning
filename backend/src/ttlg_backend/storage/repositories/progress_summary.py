"""Aggregated progress for a student (no persisted Progress row required for MVP)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import Assignment, AssignmentStatus, Lesson, LessonStatus


async def get_student_progress_summary(session: AsyncSession, student_id: UUID) -> dict:
    lessons_completed_stmt = (
        select(func.count())
        .select_from(Lesson)
        .where(
            Lesson.student_id == student_id,
            Lesson.status == LessonStatus.completed,
        )
    )
    lessons_total_stmt = select(func.count()).select_from(Lesson).where(Lesson.student_id == student_id)

    assignments_done_stmt = (
        select(func.count())
        .select_from(Assignment)
        .where(
            Assignment.student_id == student_id,
            Assignment.status == AssignmentStatus.submitted,
        )
    )
    assignments_total_stmt = (
        select(func.count())
        .select_from(Assignment)
        .where(
            Assignment.student_id == student_id,
        )
    )
    lessons_solution_checked_stmt = (
        select(func.count())
        .select_from(Lesson)
        .where(
            Lesson.student_id == student_id,
            Lesson.solution_checked.is_(True),
        )
    )

    lessons_completed = int((await session.execute(lessons_completed_stmt)).scalar_one())
    lessons_total = int((await session.execute(lessons_total_stmt)).scalar_one())
    assignments_done = int((await session.execute(assignments_done_stmt)).scalar_one())
    assignments_total = int((await session.execute(assignments_total_stmt)).scalar_one())
    lessons_solution_checked = int(
        (await session.execute(lessons_solution_checked_stmt)).scalar_one(),
    )

    return {
        "student_id": str(student_id),
        "lessons_completed": lessons_completed,
        "lessons_total": lessons_total,
        "assignments_done": assignments_done,
        "assignments_total": assignments_total,
        "lessons_solution_checked": lessons_solution_checked,
    }
