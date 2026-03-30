"""User persistence helpers."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import User, UserRole


async def create_user(
    session: AsyncSession,
    *,
    name: str,
    role: UserRole,
    telegram_id: int | None = None,
) -> User:
    user = User(name=name, role=role, telegram_id=telegram_id)
    session.add(user)
    await session.flush()
    return user


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    return await session.get(User, user_id)


async def get_student_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id, User.role == UserRole.student)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
