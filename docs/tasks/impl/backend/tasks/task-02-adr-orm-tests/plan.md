# Задача 02: ADR — ORM, миграции, тестовый раннер

## Цель

Зафиксировать в отдельном ADR выбор ORM, инструмента миграций и подхода к API-тестам / изоляции БД.

## Что меняется

- Новый файл [docs/adr/adr-002-orm-migrations-tests.md](../../../../../adr/adr-002-orm-migrations-tests.md).
- [docs/adr/README.md](../../../../../adr/README.md): строка в таблице решений.
- [docs/vision.md](../../../../../vision.md): строка в таблице «Архитектурные решения».

## Альтернативы (кратко)

- ORM: SQLAlchemy 2 async vs SQLModel vs только asyncpg.
- Миграции: Alembic vs ручной SQL.
- Тесты: `httpx.AsyncClient` vs `TestClient` (sync).

## Не в scope

- Изменение [docs/data-model.md](../../../../../data-model.md) — не требуется (PK/enum не менялись).

## Definition of Done

- ADR с контекстом, вариантами, решением, последствиями; без «висящих» TODO.
