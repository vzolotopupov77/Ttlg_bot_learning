# Итерация 5 — ORM, репозитории, интеграция в backend: итог

**Дата:** 2026-04-05  
**Статус:** ✅ Done

## Что сделано

| Задача | Артефакты |
|--------|-----------|
| 11 — Актуализация ORM-моделей | `models.py`: +3 индекса/constraint; `alembic/versions/5dcbe7dd0861_schema_review_fixes.py`; `alembic/script.py.mako` (fix) |
| 12 — Ревью репозиториев | Ревью 5 репозиториев — без проблем; `db-guide.md`: таблица ревью + раздел шаблона |
| 13 — PostgreSQL-тесты | `conftest.py` переписан; `test_dialogue_llm_error.py` мигрирован; `aiosqlite` удалён; `DATABASE_TEST_URL` в `.env.example`; `backend-db-test-create` в Makefile; раздел 7 в `db-guide.md` |
| 14 — E2E smoke + документация | E2E верифицирован; README и tasklist обновлены |

## Ключевые технические решения

| Решение | Обоснование |
|---------|-------------|
| `drop_all + create_all` per test вместо transaction rollback | asyncpg несовместим с session-scoped async fixtures при `asyncio_default_fixture_loop_scope="function"`; function-scoped изоляция надёжнее |
| `script.py.mako` исправлен | Шаблон не содержал `revision`, `down_revision` переменных — autogenerate порождало нечитаемые файлы |
| `User.telegram_id`: `unique=True` → `Index` в `__table_args__` | Устраняет ложные autogenerate-diff при каждом вызове |

## Самопроверки (агент)

### Задача 11 — Актуализация ORM-моделей

- [x] R-04: `Index("ix_messages_dialogue_created", "dialogue_id", "created_at")` добавлен в `Message.__table_args__`
- [x] R-05: `Index("ix_lessons_scheduled_at", "scheduled_at")` добавлен в `Lesson.__table_args__`
- [x] R-03: `UniqueConstraint("uq_progress_student_period")` добавлен в `Progress.__table_args__`
- [x] R-07 (`updated_at`) зафиксирован как отложенный: нет требования аудита в MVP
- [x] Ревизия `5dcbe7dd0861` не пустая: содержит `CREATE INDEX` + `ADD CONSTRAINT`
- [x] `make backend-db-reset && make backend-db-migrate` — exit 0
- [x] `make backend-test` — 17 passed
- [x] psql: `\d messages` → `ix_messages_dialogue_created` btree (dialogue_id, created_at) ✓
- [x] psql: `\d progress` → `uq_progress_student_period` UNIQUE CONSTRAINT ✓

### Задача 12 — Ревью репозиториев

- [x] Все 5 репозиториев проверены, результат зафиксирован в summary задачи
- [x] Class-based Repository (skill) — отклонён с обоснованием: функциональный подход достаточен для MVP
- [x] `make backend-test` — 17 passed (регрессий нет)
- [x] `make lint` — All checks passed
- [x] Раздел «Итоги ревью» добавлен в `db-guide.md` (раздел 3)

### Задача 13 — PostgreSQL-тесты

- [x] Паттерны skill применены; transaction rollback → `drop_all + create_all` обоснован (asyncpg/loop scope)
- [x] `TTLG_ALLOW_SQLITE_TEST` не фигурирует ни в одном файле `backend/tests/`
- [x] `aiosqlite` удалён из `backend/pyproject.toml`; `uv sync` — без ошибок
- [x] `make backend-test` — 17 passed против PostgreSQL
- [x] Раздел 7 «Тесты с PostgreSQL» добавлен в `db-guide.md`
- [x] Данные тестов не попадают в основную БД `ttlg` (изолированы в `ttlg_test`)

### Задача 14 — E2E smoke + документация

- [x] `make backend-db-reset && make backend-db-migrate && make backend-db-seed` — exit 0
- [x] `POST /v1/dialogue/message` (telegram_id=111111111) → 200 OK, непустой `text`
- [x] `SELECT role, content FROM messages LIMIT 2` → 2 строки: `user` + `assistant`
- [x] README содержит PostgreSQL-маршрут как основной; SQLite — с пометкой «только без Docker»
- [x] `tasklist-database.md` — задачи 11–14 → ✅ Done
- [x] `make check` — lint + 17 backend-test + 7 bot-test — все passed

### Итерация в целом

- [x] `make check` — зелёный
- [x] `make backend-db-reset && make backend-db-migrate && make backend-db-seed` — exit 0
- [x] README, ADR-002, `db-guide.md` актуальны
- [x] `docs/tasks/impl/database/iteration-5-orm-integration/summary.md` создан

**Не выполнено (известный долг):** bot-тесты (`tests/`) всё ещё используют SQLite — запланировано к миграции в отдельной задаче.

## Итоговая команда проверки

```
make check         → lint + 17 backend-test + 7 bot-test — все passed
make backend-db-shell → \d messages → ix_messages_dialogue_created виден
make backend-db-shell → \d progress → uq_progress_student_period виден
POST /v1/dialogue/message (telegram_id=111111111) → 200 OK; messages в psql → 2 строки
```
