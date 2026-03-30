"""User CRUD (MVP)."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.errors import api_error
from ttlg_backend.db import get_session
from ttlg_backend.dependencies import require_auth
from ttlg_backend.storage.models import UserRole
from ttlg_backend.storage.repositories import users as users_repo
from ttlg_backend.storage.repositories import progress_summary

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    role: UserRole
    telegram_id: int | None = None


class UserRead(BaseModel):
    id: UUID
    name: str
    role: UserRole
    telegram_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ProgressSummaryRead(BaseModel):
    student_id: str
    lessons_completed: int
    lessons_total: int
    assignments_done: int
    assignments_total: int


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserCreate,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead:
    user = await users_repo.create_user(
        session,
        name=body.name,
        role=body.role,
        telegram_id=body.telegram_id,
    )
    await session.commit()
    await session.refresh(user)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: UUID,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRead | JSONResponse:
    user = await users_repo.get_user_by_id(session, user_id)
    if user is None:
        return api_error(404, "not_found", "User not found")
    return UserRead.model_validate(user)


@router.get("/{user_id}/progress", response_model=ProgressSummaryRead)
async def read_user_progress(
    user_id: UUID,
    _auth: Annotated[None, Depends(require_auth)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProgressSummaryRead | JSONResponse:
    user = await users_repo.get_user_by_id(session, user_id)
    if user is None:
        return api_error(404, "not_found", "User not found")
    summary = await progress_summary.get_student_progress_summary(session, user_id)
    return ProgressSummaryRead.model_validate(summary)
