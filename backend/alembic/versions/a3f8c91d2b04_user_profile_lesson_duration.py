"""user_profile_lesson_duration

Revision ID: a3f8c91d2b04
Revises: 5dcbe7dd0861
Create Date: 2026-04-08
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "a3f8c91d2b04"
down_revision: str | None = "5dcbe7dd0861"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("class_label", sa.String(length=32), nullable=True))
    op.add_column("users", sa.Column("phone", sa.String(length=32), nullable=True))
    op.add_column("users", sa.Column("email", sa.String(length=255), nullable=True))
    op.add_column(
        "lessons",
        sa.Column(
            "duration_minutes",
            sa.SmallInteger(),
            nullable=False,
            server_default="60",
        ),
    )
    op.create_check_constraint(
        "ck_lessons_duration_positive",
        "lessons",
        "duration_minutes > 0",
    )


def downgrade() -> None:
    op.drop_constraint("ck_lessons_duration_positive", "lessons", type_="check")
    op.drop_column("lessons", "duration_minutes")
    op.drop_column("users", "email")
    op.drop_column("users", "phone")
    op.drop_column("users", "class_label")
