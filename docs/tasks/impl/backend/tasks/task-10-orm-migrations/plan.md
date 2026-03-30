# Задача 10: ORM-модели и миграции — план

## Что меняется

- Новый пакет `ttlg_backend.storage`: SQLAlchemy 2.x async-модели по [data-model.md](../../../../data-model.md).
- Каталог `backend/alembic/`, `backend/alembic.ini`, первая ревизия «initial schema».
- Цель `make backend-db-migrate`: применить миграции.

## Решения

- **PK:** UUID для всех сущностей (контракт диалога — UUID; в data-model указано «UUID / int» — фиксируем UUID в summary).
- **Enums:** PostgreSQL native: `user_role`, `lesson_status`, `assignment_status`, `dialogue_channel`, `message_role`.
- **Alembic:** async `env.py` + `DATABASE_URL` в формате `postgresql+asyncpg://`.

## Файлы

| Путь | Назначение |
|------|------------|
| `backend/src/ttlg_backend/storage/__init__.py` | Экспорт `Base`, моделей |
| `backend/src/ttlg_backend/storage/models.py` | Таблицы и enum-классы |
| `backend/alembic.ini` | Конфиг Alembic |
| `backend/alembic/env.py` | Async-миграции, импорт `Base.metadata` |
| `backend/alembic/versions/0001_initial_schema.py` | Создание таблиц и типов |

## Definition of Done

- `alembic upgrade head` без ошибок на пустой PostgreSQL.
- Модели согласованы с полями data-model (FK, nullable).
