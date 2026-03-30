# Задача 06: Каркас `backend/`, FastAPI, `/health`

## Цель

Создать пакет `ttlg_backend` в репозитории, member uv workspace; минимальное FastAPI-приложение и маршрут проверки готовности; цели Makefile для установки и запуска.

## Что меняется

- Корневой `pyproject.toml`: `[tool.uv.workspace]` с `members = [".", "backend"]`; из зависимостей `ttlg-bot` убраны пакеты, относящиеся только к backend (перенос в `backend/pyproject.toml`).
- `backend/pyproject.toml`: проект `ttlg-backend`, зависимости FastAPI/SQLAlchemy/asyncpg и т.д.
- `backend/src/ttlg_backend/main.py`: `FastAPI` app, эндпоинт `GET /health` (после задачи 07 — учёт состояния БД).
- `Makefile`: `backend-install`, `backend-run`, `.PHONY`.

## Definition of Done

- `uv sync` / `make backend-install` успешны.
- `make backend-run` поднимает uvicorn (порт **8000** по умолчанию).
- `GET http://127.0.0.1:8000/health` отвечает согласно реализации после задачи 07 (200 при доступной БД, 503 при деградации).

## Документы

- Summary: [summary.md](summary.md)
