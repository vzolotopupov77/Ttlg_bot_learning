"""Smoke tests for JWT auth and teacher routes."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from ttlg_backend.config import get_settings
from ttlg_backend.db import get_session
from ttlg_backend.main import app
from ttlg_backend.services import auth_service
from ttlg_backend.storage.models import User, UserRole


@pytest.fixture
async def teacher_with_password(pg_session):
    """Teacher user with bcrypt hash for login."""
    get_settings.cache_clear()
    ph = auth_service.hash_password("secret-pass-123")
    user = User(
        name="T",
        role=UserRole.teacher,
        email="t@example.com",
        password_hash=ph,
    )
    pg_session.add(user)
    await pg_session.commit()
    await pg_session.refresh(user)
    return user


@pytest.fixture
async def authed_client(pg_session, teacher_with_password: User):
    get_settings.cache_clear()

    async def _override_session():
        yield pg_session

    app.dependency_overrides[get_session] = _override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_session, None)
    get_settings.cache_clear()


async def test_login_and_me(authed_client: AsyncClient, teacher_with_password: User) -> None:
    r = await authed_client.post(
        "/v1/auth/login",
        json={"email": "t@example.com", "password": "secret-pass-123", "role": "teacher"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user"]["id"] == str(teacher_with_password.id)

    cookies = r.cookies
    me = await authed_client.get("/v1/auth/me", cookies=cookies)
    assert me.status_code == 200
    assert me.json()["role"] == "teacher"


async def test_teacher_schedule_requires_auth(authed_client: AsyncClient) -> None:
    r = await authed_client.get("/v1/teacher/schedule", params={"week_start": "2026-04-07"})
    assert r.status_code == 401


async def test_teacher_students_telegram_id(
    authed_client: AsyncClient,
    teacher_with_password: User,
) -> None:
    token = auth_service.create_access_token(
        subject=teacher_with_password.id,
        role=UserRole.teacher,
        secret_key=get_settings().secret_key,
        expires_minutes=60,
    )
    headers = {"Authorization": f"Bearer {token}"}
    c1 = await authed_client.post(
        "/v1/students",
        json={
            "name": "Student Telegram",
            "telegram_id": 777_001,
            "email": "tg-student@example.com",
        },
        headers=headers,
    )
    assert c1.status_code == 201, c1.text
    assert c1.json()["telegram_id"] == 777_001
    sid = c1.json()["id"]

    c_dup = await authed_client.post(
        "/v1/students",
        json={"name": "Other", "telegram_id": 777_001},
        headers=headers,
    )
    assert c_dup.status_code == 409

    cleared = await authed_client.put(
        f"/v1/students/{sid}",
        json={
            "name": "Student Telegram",
            "class_label": None,
            "phone": None,
            "email": "tg-student@example.com",
            "notes": None,
            "telegram_id": None,
        },
        headers=headers,
    )
    assert cleared.status_code == 200, cleared.text
    assert cleared.json()["telegram_id"] is None


async def test_teacher_schedule_with_bearer(
    authed_client: AsyncClient,
    teacher_with_password: User,
) -> None:
    token = auth_service.create_access_token(
        subject=teacher_with_password.id,
        role=UserRole.teacher,
        secret_key=get_settings().secret_key,
        expires_minutes=60,
    )
    r = await authed_client.get(
        "/v1/teacher/schedule",
        params={"week_start": "2026-04-07"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "items" in data
    assert data["week_start"] == "2026-04-07"
