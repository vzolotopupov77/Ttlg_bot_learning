"""FastAPI application entrypoint."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from ttlg_backend.api.assignments import router as assignments_router
from ttlg_backend.api.auth import router as auth_router
from ttlg_backend.api.dialogue import router as dialogue_router
from ttlg_backend.api.lessons import router as lessons_router
from ttlg_backend.api.settings import router as settings_router
from ttlg_backend.api.student_schedule import router as student_schedule_router
from ttlg_backend.api.students import router as students_router
from ttlg_backend.api.teacher import router as teacher_router
from ttlg_backend.api.users import router as users_router
from ttlg_backend.config import get_settings
from ttlg_backend.db import close_db, ensure_sqlite_schema, init_db, ping_db
from ttlg_backend.logging import setup_logging

logger = logging.getLogger(__name__)


def _cors_allow_origins() -> list[str]:
    raw = get_settings().cors_origins.strip()
    if not raw:
        return ["http://localhost:3000", "http://127.0.0.1:3000"]
    return [o.strip() for o in raw.split(",") if o.strip()]


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings = get_settings()
        setup_logging(settings.log_level)
        init_db(settings)
        await ensure_sqlite_schema(settings)
        if settings.database_url and not await ping_db():
            logger.warning(
                "Database unreachable at startup; GET /health will return 503 until DB is available",
            )
        yield
        await close_db()

    app = FastAPI(
        title="TTLG Backend",
        description=(
            "HTTP API ядра системы сопровождения учебного процесса: пользователи, занятия, "
            "домашние задания, диалог с ассистентом (LLM). Версия в пути: `/v1`."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_allow_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/v1")
    app.include_router(dialogue_router, prefix="/v1")
    app.include_router(users_router, prefix="/v1")
    app.include_router(lessons_router, prefix="/v1")
    app.include_router(assignments_router, prefix="/v1")
    app.include_router(teacher_router, prefix="/v1")
    app.include_router(students_router, prefix="/v1")
    app.include_router(settings_router, prefix="/v1")
    app.include_router(student_schedule_router, prefix="/v1")

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
        code = "error"
        if exc.status_code == 401:
            code = "unauthorized"
        elif exc.status_code == 403:
            code = "forbidden"
        elif exc.status_code == 404:
            code = "not_found"
        detail = exc.detail
        message = detail if isinstance(detail, str) else str(detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": code, "message": message}},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request,
        _exc: RequestValidationError,
    ) -> JSONResponse:
        logger.debug("Request validation failed")
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Проверьте введённые данные",
                }
            },
        )

    @app.get(
        "/health",
        response_model=None,
        summary="Проверка готовности сервиса",
        description=(
            'Возвращает `{"status":"ok"}`, если БД настроена и доступна. '
            "Если `DATABASE_URL` не задан или БД недоступна — **503** с телом `degraded`."
        ),
        tags=["health"],
    )
    async def health() -> Response:
        settings = get_settings()
        if settings.database_url is None:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "degraded",
                    "database": "not_configured",
                    "detail": "Set DATABASE_URL in .env (postgresql+asyncpg://...)",
                },
            )
        if await ping_db():
            return JSONResponse(content={"status": "ok"})
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "unavailable"},
        )

    return app


app = create_app()
