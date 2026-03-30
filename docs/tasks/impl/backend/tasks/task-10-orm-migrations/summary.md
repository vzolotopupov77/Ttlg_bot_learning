# Задача 10: ORM-модели и миграции — summary

**Статус:** завершена

## Сделано

- `backend/src/ttlg_backend/storage/models.py` — шесть сущностей, PostgreSQL enums, FK.
- `backend/alembic.ini`, `backend/alembic/env.py` (async), первая ревизия `0001_initial_schema.py`.
- Цель `make backend-db-migrate`: `alembic -c backend/alembic.ini upgrade head` (нужен `DATABASE_URL`).

## Отклонения от docs/data-model.md

- **Первичные ключи:** везде **UUID** (в документе указано «UUID / int»). Выбор согласован с [api-contracts.md](../../../../tech/api-contracts.md) (`dialogue_id` / `message_id` как UUID).
- **`telegram_id`:** тип в БД **BIGINT** (стабильно для Telegram ID).

## Проверка

- Локально: `make backend-db-up`, экспорт/`.env` с `DATABASE_URL`, затем `make backend-db-migrate` (ручная проверка пользователем).
