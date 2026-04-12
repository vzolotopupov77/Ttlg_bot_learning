"""Seed teacher user (Владимир / vzolotoy@mail.ru).

Revision ID: c9d0e1f2a3b4
Revises: b8c9d0e1f2a3
Create Date: 2026-04-12

"""

from __future__ import annotations

import os

import bcrypt
from alembic import op
from sqlalchemy import text

revision: str = "c9d0e1f2a3b4"
down_revision: str | None = "b8c9d0e1f2a3"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None

TEACHER_ID = "00000000-0000-0000-0000-0000000000aa"


def upgrade() -> None:
    password = os.environ.get("TEACHER_DEFAULT_PASSWORD", "changeme_teacher")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
    conn = op.get_bind()
    conn.execute(
        text(
            """
            INSERT INTO users (id, role, name, email, password_hash, created_at)
            VALUES (CAST(:id AS uuid), 'teacher', 'Владимир', 'vzolotoy@mail.ru', :ph, now())
            ON CONFLICT (id) DO NOTHING
            """
        ),
        {"id": TEACHER_ID, "ph": password_hash},
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text(f"DELETE FROM users WHERE id = '{TEACHER_ID}'::uuid"))
