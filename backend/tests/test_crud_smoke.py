"""Smoke tests for CRUD routes (SQLite)."""

from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import UUID

import pytest
from httpx import AsyncClient


@pytest.fixture
async def teacher_and_student(api_client_sqlite: AsyncClient) -> tuple[UUID, UUID]:
    t = await api_client_sqlite.post(
        "/v1/users",
        json={"name": "Teacher", "role": "teacher", "telegram_id": 100},
    )
    s = await api_client_sqlite.post(
        "/v1/users",
        json={"name": "Student", "role": "student", "telegram_id": 200},
    )
    assert t.status_code == 201 and s.status_code == 201
    return UUID(t.json()["id"]), UUID(s.json()["id"])


async def test_create_and_get_user(api_client_sqlite: AsyncClient) -> None:
    r = await api_client_sqlite.post(
        "/v1/users",
        json={"name": "U1", "role": "student", "telegram_id": 42},
    )
    assert r.status_code == 201
    uid = r.json()["id"]
    g = await api_client_sqlite.get(f"/v1/users/{uid}")
    assert g.status_code == 200
    assert g.json()["name"] == "U1"


async def test_lesson_create_get_patch(
    api_client_sqlite: AsyncClient,
    teacher_and_student: tuple[UUID, UUID],
) -> None:
    teacher_id, student_id = teacher_and_student
    when = datetime(2026, 4, 1, 12, 0, tzinfo=UTC)
    c = await api_client_sqlite.post(
        "/v1/lessons",
        json={
            "student_id": str(student_id),
            "teacher_id": str(teacher_id),
            "topic": "Algebra",
            "scheduled_at": when.isoformat(),
            "status": "scheduled",
        },
    )
    assert c.status_code == 201, c.text
    lid = c.json()["id"]
    g = await api_client_sqlite.get(f"/v1/lessons/{lid}")
    assert g.status_code == 200
    p = await api_client_sqlite.patch(
        f"/v1/lessons/{lid}/status",
        json={"status": "completed"},
    )
    assert p.status_code == 200
    assert p.json()["status"] == "completed"


async def test_assignment_create_get_patch(
    api_client_sqlite: AsyncClient,
    teacher_and_student: tuple[UUID, UUID],
) -> None:
    _, student_id = teacher_and_student
    c = await api_client_sqlite.post(
        "/v1/assignments",
        json={
            "student_id": str(student_id),
            "description": "Do exercises 1-3",
            "due_date": "2026-04-15",
            "status": "pending",
        },
    )
    assert c.status_code == 201, c.text
    aid = c.json()["id"]
    g = await api_client_sqlite.get(f"/v1/assignments/{aid}")
    assert g.status_code == 200
    p = await api_client_sqlite.patch(
        f"/v1/assignments/{aid}/status",
        json={"status": "submitted"},
    )
    assert p.status_code == 200


async def test_user_progress_summary(
    api_client_sqlite: AsyncClient,
    teacher_and_student: tuple[UUID, UUID],
) -> None:
    teacher_id, student_id = teacher_and_student
    when = datetime(2026, 4, 2, 10, 0, tzinfo=UTC)
    lr = await api_client_sqlite.post(
        "/v1/lessons",
        json={
            "student_id": str(student_id),
            "teacher_id": str(teacher_id),
            "topic": "Geometry",
            "scheduled_at": when.isoformat(),
            "status": "completed",
        },
    )
    assert lr.status_code == 201
    ar = await api_client_sqlite.post(
        "/v1/assignments",
        json={
            "student_id": str(student_id),
            "description": "HW",
            "due_date": date(2026, 4, 20).isoformat(),
            "status": "submitted",
        },
    )
    assert ar.status_code == 201
    r = await api_client_sqlite.get(f"/v1/users/{student_id}/progress")
    assert r.status_code == 200
    body = r.json()
    assert body["lessons_completed"] == 1
    assert body["assignments_done"] == 1
