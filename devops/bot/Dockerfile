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
    uv sync --package ttlg-bot --no-dev --frozen --no-install-project

COPY src src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --package ttlg-bot --no-dev --frozen

FROM python:3.12-slim-bookworm AS runtime

RUN groupadd --gid 1001 app \
    && useradd --uid 1001 --gid app --shell /usr/sbin/nologin --create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app /app

USER app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

CMD ["python", "-m", "ttlg_bot"]
