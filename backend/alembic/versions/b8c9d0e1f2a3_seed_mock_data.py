"""Seed mock data for frontend development.

Revision ID: b8c9d0e1f2a3
Revises: c7f8a2b1d4e5
Create Date: 2026-04-12

"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from alembic import op
from sqlalchemy import text

revision: str = "b8c9d0e1f2a3"
down_revision: str | None = "c7f8a2b1d4e5"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None

TEACHER_SEED_ID = "00000000-0000-0000-0000-000000000001"
S1 = "00000000-0000-0000-0000-000000000010"
S2 = "00000000-0000-0000-0000-000000000011"
S3 = "00000000-0000-0000-0000-000000000012"
S4 = "00000000-0000-0000-0000-000000000013"
D1 = "00000000-0000-0000-0000-000000000020"
RR1 = "00000000-0000-0000-0000-000000000030"


def upgrade() -> None:
    conn = op.get_bind()
    now = datetime.now(tz=UTC)

    conn.execute(
        text(
            """
            INSERT INTO users (id, role, name, telegram_id, email, class_label, phone, notes, created_at)
            VALUES
              (:tid, 'teacher', 'Seed Teacher', NULL, 'seed.teacher@example.com', NULL, NULL, NULL, now()),
              (:s1, 'student', 'Алексей Иванов', 100000001, 'alex@example.com', '10А', '+79001000101', 'ЕГЭ математика', now()),
              (:s2, 'student', 'Мария Петрова', 100000002, 'maria@example.com', '9Б', '+79001000102', NULL, now()),
              (:s3, 'student', 'Дмитрий Сидоров', 100000003, 'dmitry@example.com', '11А', NULL, NULL, now()),
              (:s4, 'student', 'Анна Козлова', 100000004, 'anna@example.com', '8В', NULL, NULL, now())
            """
        ),
        {"tid": TEACHER_SEED_ID, "s1": S1, "s2": S2, "s3": S3, "s4": S4},
    )

    lessons_rows: list[tuple[str, str, str, str, datetime, int, str, bool, bool, bool, bool, bool]] = []
    base = now.replace(hour=10, minute=0, second=0, microsecond=0)
    lesson_ids = [
        "10000000-0000-0000-0000-000000000001",
        "10000000-0000-0000-0000-000000000002",
        "10000000-0000-0000-0000-000000000003",
        "10000000-0000-0000-0000-000000000004",
        "10000000-0000-0000-0000-000000000005",
        "10000000-0000-0000-0000-000000000006",
        "10000000-0000-0000-0000-000000000007",
        "10000000-0000-0000-0000-000000000008",
        "10000000-0000-0000-0000-000000000009",
        "10000000-0000-0000-0000-00000000000A",
        "10000000-0000-0000-0000-00000000000B",
        "10000000-0000-0000-0000-00000000000C",
    ]
    for i, lid in enumerate(lesson_ids):
        st = S1 if i % 2 == 0 else S2
        when = base + timedelta(days=i - 5)
        lessons_rows.append(
            (
                lid,
                st,
                TEACHER_SEED_ID,
                f"Тема занятия {i + 1}",
                when,
                60,
                "scheduled" if i >= 8 else "completed",
                i % 3 == 0,
                i % 4 != 0,
                i % 2 == 0,
                i % 5 == 0,
                i % 6 == 0,
            ),
        )

    for row in lessons_rows:
        lid, student_id, teacher_id, topic, scheduled_at, duration, status, nf, cf, hf, sf, sc = row
        conn.execute(
            text(
                """
                INSERT INTO lessons (
                  id, student_id, teacher_id, topic, scheduled_at, duration_minutes, status, notes,
                  notification_sent, confirmed_by_student, homework_sent, solution_received, solution_checked
                )
                VALUES (
                  CAST(:id AS uuid), CAST(:sid AS uuid), CAST(:tid AS uuid), :topic, :at, :dur,
                  CAST(:status AS lesson_status), NULL,
                  :nf, :cf, :hf, :sf, :sc
                )
                """
            ),
            {
                "id": lid,
                "sid": student_id,
                "tid": teacher_id,
                "topic": topic,
                "at": scheduled_at,
                "dur": duration,
                "status": status,
                "nf": nf,
                "cf": cf,
                "hf": hf,
                "sf": sf,
                "sc": sc,
            },
        )

    conn.execute(
        text(
            """
            INSERT INTO system_settings (key, value) VALUES
              ('teacher_name', 'Владимир'),
              ('default_lesson_duration_minutes', '60'),
              ('lesson_reminder_hours_before', '24'),
              ('homework_reminder_hours_before', '48')
            """
        )
    )

    conn.execute(
        text(
            """
            INSERT INTO dialogues (id, student_id, channel, started_at)
            VALUES (CAST(:id AS uuid), CAST(:sid AS uuid), 'telegram', now())
            """
        ),
        {"id": D1, "sid": S1},
    )

    msg_ids = [
        "20000000-0000-0000-0000-000000000001",
        "20000000-0000-0000-0000-000000000002",
        "20000000-0000-0000-0000-000000000003",
        "20000000-0000-0000-0000-000000000004",
        "20000000-0000-0000-0000-000000000005",
        "20000000-0000-0000-0000-000000000006",
    ]
    for i, mid in enumerate(msg_ids):
        role = "user" if i % 2 == 0 else "assistant"
        content = f"Сообщение {i + 1} в диалоге"
        created_at = now - timedelta(minutes=i * 10)
        conn.execute(
            text(
                """
                INSERT INTO messages (id, dialogue_id, role, content, created_at)
                VALUES (CAST(:id AS uuid), CAST(:did AS uuid), CAST(:role AS message_role), :content, :at)
                """
            ),
            {"id": mid, "did": D1, "role": role, "content": content, "at": created_at},
        )

    first_lesson_id = lesson_ids[0]
    conn.execute(
        text(
            """
            INSERT INTO reschedule_requests (id, lesson_id, student_id, proposed_time, requested_at, status)
            VALUES (CAST(:id AS uuid), CAST(:lid AS uuid), CAST(:sid AS uuid), :prop, now(), 'pending')
            """
        ),
        {
            "id": RR1,
            "lid": first_lesson_id,
            "sid": S1,
            "prop": now + timedelta(days=2),
        },
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text(f"DELETE FROM reschedule_requests WHERE id = '{RR1}'::uuid"))
    conn.execute(text(f"DELETE FROM messages WHERE dialogue_id = '{D1}'::uuid"))
    conn.execute(text(f"DELETE FROM dialogues WHERE id = '{D1}'::uuid"))
    conn.execute(text(f"DELETE FROM lessons WHERE teacher_id = '{TEACHER_SEED_ID}'::uuid"))
    conn.execute(
        text(
            """
            DELETE FROM system_settings WHERE key IN (
              'teacher_name','default_lesson_duration_minutes','lesson_reminder_hours_before','homework_reminder_hours_before'
            )
            """
        )
    )
    conn.execute(
        text(
            f"""
            DELETE FROM users WHERE id IN (
              '{TEACHER_SEED_ID}'::uuid,
              '{S1}'::uuid,
              '{S2}'::uuid,
              '{S3}'::uuid,
              '{S4}'::uuid
            )
            """
        )
    )
