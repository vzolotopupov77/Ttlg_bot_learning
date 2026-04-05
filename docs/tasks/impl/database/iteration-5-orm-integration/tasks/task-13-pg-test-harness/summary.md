# Задача 13: Тестовый стенд с PostgreSQL — итог

**Дата:** 2026-04-05  
**Статус:** ✅ Done

## Что сделано

| Артефакт | Изменение |
|----------|-----------|
| `backend/tests/conftest.py` | Полностью переписан: убраны `init_db`, `ensure_sqlite_schema`, `reset_engine`; добавлены `pg_session`, `api_client_sqlite` (alias), `dialogue_client` |
| `backend/tests/test_dialogue_llm_error.py` | Мигрирован с `TTLG_ALLOW_SQLITE_TEST` / SQLite на `pg_session` |
| `backend/pyproject.toml` | Удалён `aiosqlite` из `[dependency-groups] dev` |
| Root `pyproject.toml` | Добавлен `aiosqlite` в `[dependency-groups] dev` (нужен bot-тестам, которые ещё используют SQLite) |
| `.env.example` | Добавлена `DATABASE_TEST_URL` с комментарием |
| `Makefile` | Добавлена цель `backend-db-test-create` |
| `docs/tech/db-guide.md` | Добавлен раздел 7 «Тесты с PostgreSQL» |
| `alembic/script.py.mako` | Исправлен шаблон (побочно в задаче 12) |

## Технические решения

| Вопрос | Решение |
|--------|---------|
| testcontainers vs существующий контейнер | Существующий (без новых зависимостей) |
| Изоляция | `drop_all + create_all` per test (function scope) |
| Session scope | **Отклонено**: asyncpg несовместим с session-scoped async fixtures при `asyncio_default_fixture_loop_scope="function"` |
| `asyncio_default_fixture_loop_scope` | Оставлено "function" (не меняли) |
| `aiosqlite` | Удалён |
| `TTLG_ALLOW_SQLITE_TEST` | Убран из тестов backend; в `db.py` и `config.py` оставлен для bot-тестов |

## Самопроверка

- [x] `TTLG_ALLOW_SQLITE_TEST` не фигурирует ни в одном `backend/tests/` файле
- [x] `aiosqlite` удалён из `backend/pyproject.toml`
- [x] `make backend-test` — 17 passed против PostgreSQL
- [x] `make backend-db-shell` → `SELECT count(*) FROM users;` → 0 (тесты не оставляют мусора в основной БД)
- [x] Раздел «Тесты с PostgreSQL» добавлен в `db-guide.md`
