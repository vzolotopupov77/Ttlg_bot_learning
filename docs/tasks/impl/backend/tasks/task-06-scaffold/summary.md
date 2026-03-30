# Задача 06: Summary

## Сделано

- Добавлен member uv workspace `backend/` с пакетом `ttlg-backend` (`backend/src/ttlg_backend/`).
- Корневой [pyproject.toml](../../../../../../pyproject.toml): `[tool.uv.workspace]` с `members = [".", "backend"]`; из зависимостей бота убраны FastAPI/SQLAlchemy/asyncpg/Alembic/uvicorn (перенесены в backend).
- [Makefile](../../../../../../Makefile): цели `install` (`uv sync --all-packages`), `backend-install`, `backend-run` (uvicorn на **127.0.0.1:8000**).
- FastAPI-приложение и маршрут `GET /health` реализованы в задаче 06 совместно с задачей 07 (конфиг, БД, деградация при недоступной БД).

## Отклонения

- Маршрут `/health` после объединения с задачей 07 не возвращает только `{"status":"ok"}` без БД — при недоступной БД допустим **503** (см. план задачи 07).

## Проверка

- `uv run --package ttlg-backend python -c "from ttlg_backend.main import app; print(app.title)"` — успех.
