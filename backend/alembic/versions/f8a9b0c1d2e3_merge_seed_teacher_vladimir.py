"""Merge Vladimir into seed teacher: update …0001, drop duplicate …00aa.

Revision ID: f8a9b0c1d2e3
Revises: e1f2a3b4c5d6
Create Date: 2026-04-22

Для БД, созданных до объединения двух учителей в одном сид-пользователе.
"""

from __future__ import annotations

import os

import bcrypt
from alembic import op
from sqlalchemy import text

revision: str = "f8a9b0c1d2e3"
down_revision: str | None = "e1f2a3b4c5d6"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None

TEACHER_SEED_ID = "00000000-0000-0000-0000-000000000001"
VLADIMIR_DUPLICATE_ID = "00000000-0000-0000-0000-0000000000aa"


def upgrade() -> None:
    password = os.environ.get("TEACHER_DEFAULT_PASSWORD", "changeme_teacher")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE users
            SET name = 'Владимир',
                email = 'vzolotoy@mail.ru',
                password_hash = :ph
            WHERE id = CAST(:id AS uuid)
              AND role = 'teacher'
            """
        ),
        {"id": TEACHER_SEED_ID, "ph": password_hash},
    )
    conn.execute(
        text("DELETE FROM users WHERE id = CAST(:id AS uuid)"),
        {"id": VLADIMIR_DUPLICATE_ID},
    )


def downgrade() -> None:
    pass
