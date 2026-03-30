"""JSON error responses aligned with docs/api-conventions.md."""

from __future__ import annotations

from fastapi.responses import JSONResponse


def api_error(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )
