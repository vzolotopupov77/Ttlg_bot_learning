"""Async SQLAlchemy engine and session factory."""

from __future__ import annotations

import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ttlg_backend.config import Settings
from ttlg_backend.storage.models import Base

logger = logging.getLogger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def init_db(settings: Settings) -> None:
    """Create engine and session factory (idempotent). Skips if DATABASE_URL unset."""
    global _engine, _session_factory
    if _engine is not None:
        return
    if not settings.database_url:
        logger.warning(
            "DATABASE_URL is not set; database disabled. Set it in .env (see .env.example).",
        )
        return
    _engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False)


def get_engine() -> AsyncEngine | None:
    return _engine


async def reset_engine() -> None:
    """Dispose engine and clear factories (tests / reload)."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None


async def ensure_sqlite_schema(settings: Settings) -> None:
    """Create tables for in-memory SQLite test DB (no Alembic)."""
    if not settings.allow_sqlite_test:
        return
    url = settings.database_url or ""
    if not url.startswith("sqlite"):
        return
    if _engine is None:
        return
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await reset_engine()


async def ping_db() -> bool:
    """Return True if database accepts a trivial query."""
    if _engine is None:
        return False
    try:
        async with _engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:  # noqa: BLE001 — deliberate broad catch for health
        logger.warning("Database ping failed: %s", type(exc).__name__)
        return False


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if _session_factory is None:
        msg = "Database not initialized; call init_db first"
        raise RuntimeError(msg)
    async with _session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
