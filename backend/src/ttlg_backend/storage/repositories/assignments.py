"""Assignment persistence helpers."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import Assignment, AssignmentStatus


async def create_assignment(
    session: AsyncSession,
    *,
    student_id: UUID,
    description: str,
    due_date: date,
    lesson_id: UUID | None = None,
    status: AssignmentStatus = AssignmentStatus.pending,
) -> Assignment:
    assignment = Assignment(
        student_id=student_id,
        lesson_id=lesson_id,
        description=description,
        due_date=due_date,
        status=status,
    )
    session.add(assignment)
    await session.flush()
    return assignment


async def get_assignment_by_id(session: AsyncSession, assignment_id: UUID) -> Assignment | None:
    return await session.get(Assignment, assignment_id)


async def update_assignment_status(
    session: AsyncSession,
    assignment_id: UUID,
    status: AssignmentStatus,
) -> Assignment | None:
    assignment = await session.get(Assignment, assignment_id)
    if assignment is None:
        return None
    assignment.status = status
    await session.flush()
    return assignment


async def list_recent_assignments_for_student(
    session: AsyncSession,
    student_id: UUID,
    *,
    limit: int = 8,
) -> list[Assignment]:
    stmt = (
        select(Assignment).where(Assignment.student_id == student_id).order_by(Assignment.due_date.desc()).limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
