"""User persistence helpers."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import User, UserRole


async def create_user(
    session: AsyncSession,
    *,
    name: str,
    role: UserRole,
    telegram_id: int | None = None,
    class_label: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    password_hash: str | None = None,
    notes: str | None = None,
) -> User:
    user = User(
        name=name,
        role=role,
        telegram_id=telegram_id,
        class_label=class_label,
        phone=phone,
        email=email,
        password_hash=password_hash,
        notes=notes,
    )
    session.add(user)
    await session.flush()
    return user


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    return await session.get(User, user_id)


async def get_student_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id, User.role == UserRole.student)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email_and_role(
    session: AsyncSession,
    *,
    email: str,
    role: UserRole,
) -> User | None:
    normalized = email.strip().lower()
    stmt = select(User).where(func.lower(User.email) == normalized, User.role == role)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(session: AsyncSession, *, email: str) -> User | None:
    normalized = email.strip().lower()
    stmt = select(User).where(func.lower(User.email) == normalized)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def list_students(
    session: AsyncSession,
    *,
    limit: int,
    offset: int,
) -> tuple[list[User], int]:
    base = select(User).where(User.role == UserRole.student)
    count_stmt = select(func.count()).select_from(User).where(User.role == UserRole.student)
    total = int((await session.execute(count_stmt)).scalar_one())
    stmt = base.order_by(User.name.asc()).offset(offset).limit(limit)
    rows = await session.execute(stmt)
    return list(rows.scalars().all()), total


async def delete_user(session: AsyncSession, user_id: UUID) -> bool:
    user = await session.get(User, user_id)
    if user is None:
        return False
    await session.delete(user)
    await session.flush()
    return True


async def update_user_fields(
    session: AsyncSession,
    user: User,
    *,
    name: str | None = None,
    class_label: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    notes: str | None = None,
) -> User:
    if name is not None:
        user.name = name
    if class_label is not None:
        user.class_label = class_label
    if phone is not None:
        user.phone = phone
    if email is not None:
        user.email = email
    if notes is not None:
        user.notes = notes
    await session.flush()
    return user
