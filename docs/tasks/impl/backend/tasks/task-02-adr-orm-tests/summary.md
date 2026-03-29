# Задача 02: ADR — ORM, миграции, тестовый раннер — summary

## Сделано

- Добавлен [docs/adr/adr-002-orm-migrations-tests.md](../../../../../adr/adr-002-orm-migrations-tests.md):
  - ORM: **SQLAlchemy 2.x async**; отклонены как основной слой SQLModel и «только asyncpg».
  - Миграции: **Alembic**; путь к каталогу ревизий — при каркасе backend.
  - Тесты: **pytest**, **pytest-asyncio**, **httpx.AsyncClient**; sync `TestClient` не основной выбор.
  - Изоляция БД в тестах — уточняется в задаче 08 (без противоречий ADR).
- Обновлены [docs/adr/README.md](../../../../../adr/README.md) и таблица ADR в [docs/vision.md](../../../../../vision.md).

## Не сделано намеренно

- [docs/data-model.md](../../../../../data-model.md) не менялся (PK/enum без изменений).

## Отклонения

- Нет.
