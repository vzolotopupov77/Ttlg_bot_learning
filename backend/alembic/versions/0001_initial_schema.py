"""Initial schema: users, lessons, assignments, progress, dialogues, messages.

Revision ID: 0001
Revises:
Create Date: 2026-03-30

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = postgresql.ENUM("student", "teacher", name="user_role", create_type=True)
    lesson_status = postgresql.ENUM("scheduled", "completed", "cancelled", name="lesson_status", create_type=True)
    assignment_status = postgresql.ENUM("pending", "submitted", "overdue", name="assignment_status", create_type=True)
    dialogue_channel = postgresql.ENUM("telegram", "web", name="dialogue_channel", create_type=True)
    message_role = postgresql.ENUM("user", "assistant", name="message_role", create_type=True)

    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    lesson_status.create(bind, checkfirst=True)
    assignment_status.create(bind, checkfirst=True)
    dialogue_channel.create(bind, checkfirst=True)
    message_role.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index(op.f("ix_users_telegram_id"), "users", ["telegram_id"], unique=True)

    op.create_table(
        "lessons",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("teacher_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("topic", sa.String(length=512), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", lesson_status, nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["teacher_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_lessons_student_id"), "lessons", ["student_id"], unique=False)
    op.create_index(op.f("ix_lessons_teacher_id"), "lessons", ["teacher_id"], unique=False)

    op.create_table(
        "assignments",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("lesson_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("student_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", assignment_status, nullable=False),
        sa.ForeignKeyConstraint(["lesson_id"], ["lessons.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_assignments_lesson_id"), "assignments", ["lesson_id"], unique=False)
    op.create_index(op.f("ix_assignments_student_id"), "assignments", ["student_id"], unique=False)

    op.create_table(
        "progress",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("lessons_completed", sa.Integer(), nullable=False),
        sa.Column("assignments_done", sa.Integer(), nullable=False),
        sa.Column("assignments_total", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_progress_student_id"), "progress", ["student_id"], unique=False)

    op.create_table(
        "dialogues",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("channel", dialogue_channel, nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_dialogues_student_id"), "dialogues", ["student_id"], unique=False)

    op.create_table(
        "messages",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("dialogue_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("role", message_role, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["dialogue_id"], ["dialogues.id"], ondelete="CASCADE"),
    )
    op.create_index(op.f("ix_messages_dialogue_id"), "messages", ["dialogue_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_messages_dialogue_id"), table_name="messages")
    op.drop_table("messages")

    op.drop_index(op.f("ix_dialogues_student_id"), table_name="dialogues")
    op.drop_table("dialogues")

    op.drop_index(op.f("ix_progress_student_id"), table_name="progress")
    op.drop_table("progress")

    op.drop_index(op.f("ix_assignments_student_id"), table_name="assignments")
    op.drop_index(op.f("ix_assignments_lesson_id"), table_name="assignments")
    op.drop_table("assignments")

    op.drop_index(op.f("ix_lessons_teacher_id"), table_name="lessons")
    op.drop_index(op.f("ix_lessons_student_id"), table_name="lessons")
    op.drop_table("lessons")

    op.drop_index(op.f("ix_users_telegram_id"), table_name="users")
    op.drop_table("users")

    message_role = postgresql.ENUM(name="message_role")
    message_role.drop(op.get_bind(), checkfirst=True)
    dialogue_channel = postgresql.ENUM(name="dialogue_channel")
    dialogue_channel.drop(op.get_bind(), checkfirst=True)
    assignment_status = postgresql.ENUM(name="assignment_status")
    assignment_status.drop(op.get_bind(), checkfirst=True)
    lesson_status = postgresql.ENUM(name="lesson_status")
    lesson_status.drop(op.get_bind(), checkfirst=True)
    user_role = postgresql.ENUM(name="user_role")
    user_role.drop(op.get_bind(), checkfirst=True)
