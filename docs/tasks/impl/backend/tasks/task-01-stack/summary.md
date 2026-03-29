# Задача 01: Согласовать и зафиксировать backend-стек — summary

## Сделано

- Обновлён [docs/vision.md](../../../../../vision.md):
  - Backend: **FastAPI** + **pydantic-settings**; ссылка на [ADR-002](../../../../../adr/adr-002-orm-migrations-tests.md) для деталей по данным и тестам.
  - Слой данных: **PostgreSQL** с первого дня, ссылка на [ADR-001](../../../../../adr/adr-001-database.md).
  - Таблица «Технологии»: **uvicorn**, **asyncpg**, **SQLAlchemy** 2.x async, **Alembic**, **pytest** / **httpx** / **pytest-asyncio**.
- Структура `backend/src/ttlg_backend/` в vision без изменений по составу каталогов (`api/`, `services/`, `storage/`, `llm/`).
- В корневом [pyproject.toml](../../../../../../pyproject.toml): **fastapi**, **uvicorn[standard]**, **sqlalchemy[asyncio]**, **asyncpg**, **alembic** в основных зависимостях; **pytest**, **pytest-asyncio**, **httpx** в extra `dev` (`uv sync --extra dev`).

## Примечание

- Подзадача по `pyproject.toml` сначала была отложена по внутреннему черновику плана; по [tasklist-backend.md](../../../../tasklist-backend.md) она часть задачи 01 — закрыта этим дополнением.

## Отклонения

- Нет.

## Проверка

- Vision согласован с ADR-001 и ADR-002.
