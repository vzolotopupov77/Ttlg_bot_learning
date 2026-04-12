"""Key-value system settings."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import SystemSetting


async def get_all(session: AsyncSession) -> dict[str, str]:
    stmt = select(SystemSetting)
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return {r.key: r.value for r in rows}


async def upsert_many(session: AsyncSession, items: dict[str, str]) -> None:
    for key, value in items.items():
        existing = await session.get(SystemSetting, key)
        if existing is None:
            session.add(SystemSetting(key=key, value=value))
        else:
            existing.value = value
    await session.flush()
