"""Shared FastAPI dependencies (DB session, JWT user)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends, Header, HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.config import Settings, get_settings
from ttlg_backend.db import get_session
from ttlg_backend.services import auth_service
from ttlg_backend.storage.models import User, UserRole

ACCESS_TOKEN_COOKIE = "ttlg_access_token"


def _bearer_from_header(authorization: str | None) -> str | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    return authorization.removeprefix("Bearer ").strip() or None


def get_token_from_cookie_or_header(
    authorization: Annotated[str | None, Header()] = None,
    access_token: Annotated[str | None, Cookie(alias=ACCESS_TOKEN_COOKIE)] = None,
) -> str | None:
    if access_token:
        return access_token
    return _bearer_from_header(authorization)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
    token: Annotated[str | None, Depends(get_token_from_cookie_or_header)] = None,
) -> User:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется вход",
        )
    try:
        payload = auth_service.decode_token(token, settings.secret_key)
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
            )
        user_id = UUID(str(sub))
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
        ) from None

    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
    role_in_token = payload.get("role")
    if role_in_token is not None and role_in_token != user.role.value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Роль в сессии не совпадает с данными",
        )
    return user


async def require_teacher(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if user.role != UserRole.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужна роль преподавателя",
        )
    return user


async def require_student(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нужна роль ученика",
        )
    return user
