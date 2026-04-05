# Задача 13: Тестовый стенд с PostgreSQL — план

**Дата:** 2026-04-05

## Цель

Настроить тесты backend против реального PostgreSQL. Убрать SQLite. Обеспечить изоляцию данных между тестами.

## Подход

- Отдельная база `ttlg_test` в существующем контейнере (`testcontainers` не вводим)
- Изоляция: `drop_all + create_all` per test (function-scoped `pg_engine`)
- Причина: session-scoped async fixtures несовместимы с asyncpg при `asyncio_default_fixture_loop_scope="function"`

## Файлы

- `backend/tests/conftest.py` — новые PostgreSQL-фикстуры
- `backend/tests/test_dialogue_llm_error.py` — мигрирован с SQLite на pg_session
- `backend/pyproject.toml` — убрать `aiosqlite`
- `.env.example` — добавить `DATABASE_TEST_URL`
- `Makefile` — добавить `backend-db-test-create`
- `docs/tech/db-guide.md` — раздел «Тесты с PostgreSQL»
