"""FastAPI application entrypoint."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response

from ttlg_backend.api.assignments import router as assignments_router
from ttlg_backend.api.dialogue import router as dialogue_router
from ttlg_backend.api.lessons import router as lessons_router
from ttlg_backend.api.users import router as users_router
from ttlg_backend.config import get_settings
from ttlg_backend.db import close_db, ensure_sqlite_schema, init_db, ping_db
from ttlg_backend.logging import setup_logging

logger = logging.getLogger(__name__)


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
        title="ttlg-backend",
        lifespan=lifespan,
    )

    app.include_router(dialogue_router, prefix="/v1")
    app.include_router(users_router, prefix="/v1")
    app.include_router(lessons_router, prefix="/v1")
    app.include_router(assignments_router, prefix="/v1")

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
                    "message": "Request validation failed",
                }
            },
        )

    @app.get("/health", response_model=None)
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
