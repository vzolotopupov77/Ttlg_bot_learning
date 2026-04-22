"""Remove duplicate Vladimir teacher row (merged into seed teacher id …0001).

Revision ID: c9d0e1f2a3b4
Revises: b8c9d0e1f2a3
Create Date: 2026-04-12

Previously this revision inserted a second teacher (…00aa). Seed teacher …0001
now carries Владимир / vzolotoy@mail.ru in b8c9d0e1f2a3; this step only deletes
the duplicate UUID if present (e.g. after upgrading from older migrations).
"""

from __future__ import annotations

from alembic import op
from sqlalchemy import text

revision: str = "c9d0e1f2a3b4"
down_revision: str | None = "b8c9d0e1f2a3"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None

# Было вставлено в старой версии этой миграции — больше не используется.
VLADIMIR_DUPLICATE_ID = "00000000-0000-0000-0000-0000000000aa"


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text("DELETE FROM users WHERE id = CAST(:id AS uuid)"),
        {"id": VLADIMIR_DUPLICATE_ID},
    )


def downgrade() -> None:
    # Восстановление второго учителя намеренно не делаем: единственный сид-учитель — …0001.
    pass
