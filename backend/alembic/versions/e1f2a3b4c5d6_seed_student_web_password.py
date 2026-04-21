"""Set password_hash for seed student (alex@example.com) for web login.

Revision ID: e1f2a3b4c5d6
Revises: c9d0e1f2a3b4
Create Date: 2026-04-21

"""

from __future__ import annotations

import os

import bcrypt
from alembic import op
from sqlalchemy import text

revision: str = "e1f2a3b4c5d6"
down_revision: str | None = "c9d0e1f2a3b4"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None

# Same UUID as b8c9d0e1f2a3_seed_mock_data: Алексей Иванов
STUDENT_ID = "00000000-0000-0000-0000-000000000010"


def upgrade() -> None:
    password = os.environ.get("STUDENT_DEFAULT_PASSWORD", "changeme_student")
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE users
            SET password_hash = :ph
            WHERE id = CAST(:id AS uuid)
              AND email = 'alex@example.com'
              AND role = 'student'
            """
        ),
        {"id": STUDENT_ID, "ph": password_hash},
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE users
            SET password_hash = NULL
            WHERE id = CAST(:id AS uuid)
              AND email = 'alex@example.com'
            """
        ),
        {"id": STUDENT_ID},
    )
