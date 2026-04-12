"""Auth: login (JWT cookie), logout, current user."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.api.deps import ACCESS_TOKEN_COOKIE, get_current_user
from ttlg_backend.api.errors import api_error
from ttlg_backend.config import Settings, get_settings
from ttlg_backend.db import get_session
from ttlg_backend.services import auth_service
from ttlg_backend.storage.models import User, UserRole
from ttlg_backend.storage.repositories import users as users_repo

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginBody(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)
    role: UserRole


class UserPublic(BaseModel):
    id: str
    name: str
    role: UserRole

    model_config = {"from_attributes": False}


class LoginResponse(BaseModel):
    user: UserPublic


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Вход (JWT в httpOnly cookie)",
)
async def login(
    body: LoginBody,
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> LoginResponse | Response:
    user = await users_repo.get_user_by_email_and_role(session, email=str(body.email), role=body.role)
    if user is None or not auth_service.verify_password(body.password, user.password_hash):
        return api_error(401, "invalid_credentials", "Invalid email, password, or role")

    token = auth_service.create_access_token(
        subject=user.id,
        role=user.role,
        secret_key=settings.secret_key,
        expires_minutes=settings.access_token_expire_minutes,
    )
    max_age = settings.access_token_expire_minutes * 60
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=token,
        httponly=True,
        max_age=max_age,
        samesite="lax",
        secure=False,
        path="/",
    )
    return LoginResponse(
        user=UserPublic(id=str(user.id), name=user.name, role=user.role),
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Выход (очистка cookie)",
)
async def logout(response: Response) -> Response:
    response.delete_cookie(key=ACCESS_TOKEN_COOKIE, path="/")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Текущий пользователь",
)
async def me(
    user: Annotated[User, Depends(get_current_user)],
) -> UserPublic:
    return UserPublic(id=str(user.id), name=user.name, role=user.role)
