# syntax=docker/dockerfile:1
# Контекст сборки: корень репозитория.
FROM python:3.12-slim-bookworm AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY backend/pyproject.toml backend/pyproject.toml

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package ttlg-backend --no-dev --frozen --no-install-project

COPY backend/src backend/src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package ttlg-backend --no-dev --frozen

COPY backend/alembic backend/alembic
COPY backend/alembic.ini backend/alembic.ini

FROM python:3.12-slim-bookworm AS runtime

RUN groupadd --gid 1001 app \
    && useradd --uid 1001 --gid app --shell /usr/sbin/nologin --create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app /app

USER app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)"

CMD ["uvicorn", "ttlg_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
