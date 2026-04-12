"""frontend_iteration1_schema: auth fields, lesson flags, reschedule_requests, system_settings.

Revision ID: c7f8a2b1d4e5
Revises: a3f8c91d2b04
Create Date: 2026-04-12

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "c7f8a2b1d4e5"
down_revision: str | None = "a3f8c91d2b04"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("password_hash", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("notes", sa.Text(), nullable=True))

    op.add_column(
        "lessons",
        sa.Column("notification_sent", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "lessons",
        sa.Column("confirmed_by_student", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "lessons",
        sa.Column("homework_sent", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "lessons",
        sa.Column("solution_received", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "lessons",
        sa.Column("solution_checked", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "reschedule_requests",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("lesson_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("student_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("proposed_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("requested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("status", sa.Text(), server_default="pending", nullable=False),
        sa.CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name="ck_reschedule_requests_status"),
        sa.ForeignKeyConstraint(["lesson_id"], ["lessons.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reschedule_requests_lesson_id", "reschedule_requests", ["lesson_id"], unique=False)
    op.create_index("ix_reschedule_requests_student_id", "reschedule_requests", ["student_id"], unique=False)

    op.create_table(
        "system_settings",
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )


def downgrade() -> None:
    op.drop_table("system_settings")
    op.drop_index("ix_reschedule_requests_student_id", table_name="reschedule_requests")
    op.drop_index("ix_reschedule_requests_lesson_id", table_name="reschedule_requests")
    op.drop_table("reschedule_requests")

    op.drop_column("lessons", "solution_checked")
    op.drop_column("lessons", "solution_received")
    op.drop_column("lessons", "homework_sent")
    op.drop_column("lessons", "confirmed_by_student")
    op.drop_column("lessons", "notification_sent")

    op.drop_column("users", "notes")
    op.drop_column("users", "password_hash")
