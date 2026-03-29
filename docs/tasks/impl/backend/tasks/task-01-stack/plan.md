# Задача 01: Согласовать и зафиксировать backend-стек

## Цель

Зафиксировать пакеты и архитектурные ориентиры backend согласно [docs/vision.md](../../../../../vision.md) и [ADR-001](../../../../../adr/adr-001-database.md).

## Что меняется

- [docs/vision.md](../../../../../vision.md): FastAPI без оговорки «или аналог»; PostgreSQL как основная СУБД (ссылка на ADR-001); расширенная таблица технологий (ORM, драйвер, миграции, тесты).
- [pyproject.toml](../../../../../../pyproject.toml): зависимости backend в `[project.dependencies]`; тестовый стек в `[project.optional-dependencies] dev`.
- Структура `backend/src/ttlg_backend/` (`api/`, `services/`, `storage/`, `llm/`) — подтверждена в vision.

## Зависимости (зафиксированы в vision)

| Назначение | Пакеты |
|------------|--------|
| HTTP | `fastapi`, `uvicorn[standard]` |
| БД async | `asyncpg`, `sqlalchemy[asyncio]` 2.x |
| Миграции | `alembic` |
| Конфиг | `pydantic-settings` |
| Тесты | `pytest`, `httpx`, `pytest-asyncio` |

## Definition of Done

- Vision согласован с ADR-001; противоречий с будущим ADR-002 нет (стек описан на уровне имён технологий).
