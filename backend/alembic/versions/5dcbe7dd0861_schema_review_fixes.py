"""schema_review_fixes

Revision ID: 5dcbe7dd0861
Revises: 0001
Create Date: 2026-04-05 15:20:18.922096
"""

from __future__ import annotations

from alembic import op

revision: str = "5dcbe7dd0861"
down_revision: str | None = "0001"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    op.create_index("ix_lessons_scheduled_at", "lessons", ["scheduled_at"], unique=False)
    op.create_index("ix_messages_dialogue_created", "messages", ["dialogue_id", "created_at"], unique=False)
    op.create_unique_constraint("uq_progress_student_period", "progress", ["student_id", "period_start", "period_end"])


def downgrade() -> None:
    op.drop_constraint("uq_progress_student_period", "progress", type_="unique")
    op.drop_index("ix_messages_dialogue_created", table_name="messages")
    op.drop_index("ix_lessons_scheduled_at", table_name="lessons")
