# Итерация 5 — ORM, репозитории, интеграция в backend: план

**Дата:** 2026-04-05  
**Статус:** ✅ Done

## Цель

Привести ORM-модели и репозитории в соответствие с итогами ревью схемы; настроить тесты против PostgreSQL; верифицировать полный сценарий end-to-end на PostgreSQL.

## Ценность

После итерации backend полностью работает на PostgreSQL — без SQLite-заглушки; тесты гарантируют отсутствие регрессий при изменении схемы.

## Состав задач

| № | Задача | Статус |
|---|--------|--------|
| 11 | Актуализация ORM-моделей | ✅ Done |
| 12 | Ревью и доработка репозиториев | ✅ Done |
| 13 | Тестовый стенд с PostgreSQL | ✅ Done |
| 14 | End-to-end smoke на PostgreSQL + документация | ✅ Done |

## Артефакты

- `backend/src/ttlg_backend/storage/models.py` — новые индексы и constraint
- `backend/alembic/versions/5dcbe7dd0861_schema_review_fixes.py` — ревизия из задачи 11
- `backend/src/ttlg_backend/storage/repositories/*.py` — при необходимости правки
- `backend/tests/conftest.py` — PostgreSQL-фикстуры
- `backend/pyproject.toml` — убрать `aiosqlite`
- `.env.example` — `DATABASE_TEST_URL`
- `docs/tech/db-guide.md` — разделы «Репозитории» и «Тесты с PostgreSQL»
- `README.md`, `docs/vision.md`, `docs/plan.md` — финальные обновления
