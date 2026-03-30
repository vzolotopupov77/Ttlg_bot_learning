"""Assignment CRUD (MVP)."""

from __future__ import annotations

from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.errors import api_error
from ttlg_backend.db import get_session
from ttlg_backend.dependencies import require_auth
from ttlg_backend.storage.models import AssignmentStatus
from ttlg_backend.storage.repositories import assignments as assignments_repo

router = APIRouter(prefix="/assignments", tags=["assignments"])


class AssignmentCreate(BaseModel):
    student_id: UUID
    description: str = Field(..., min_length=1)
    due_date: date
    lesson_id: UUID | None = None
    status: AssignmentStatus = AssignmentStatus.pending


class AssignmentRead(BaseModel):
    id: UUID
    lesson_id: UUID | None
    student_id: UUID
    description: str
    due_date: date
    status: AssignmentStatus

    model_config = {"from_attributes": True}


class AssignmentStatusPatch(BaseModel):
    status: AssignmentStatus


@router.post("", response_model=AssignmentRead, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    body: AssignmentCreate,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AssignmentRead:
    assignment = await assignments_repo.create_assignment(
        session,
        student_id=body.student_id,
        lesson_id=body.lesson_id,
        description=body.description,
        due_date=body.due_date,
        status=body.status,
    )
    await session.commit()
    await session.refresh(assignment)
    return AssignmentRead.model_validate(assignment)


@router.get("/{assignment_id}", response_model=AssignmentRead)
async def read_assignment(
    assignment_id: UUID,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AssignmentRead | JSONResponse:
    assignment = await assignments_repo.get_assignment_by_id(session, assignment_id)
    if assignment is None:
        return api_error(404, "not_found", "Assignment not found")
    return AssignmentRead.model_validate(assignment)


@router.patch("/{assignment_id}/status", response_model=AssignmentRead)
async def patch_assignment_status(
    assignment_id: UUID,
    body: AssignmentStatusPatch,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AssignmentRead | JSONResponse:
    assignment = await assignments_repo.update_assignment_status(
        session,
        assignment_id,
        body.status,
    )
    if assignment is None:
        return api_error(404, "not_found", "Assignment not found")
    await session.commit()
    await session.refresh(assignment)
    return AssignmentRead.model_validate(assignment)
