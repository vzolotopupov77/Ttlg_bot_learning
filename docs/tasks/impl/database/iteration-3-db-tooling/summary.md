# Summary: Итерация 3 — Инструменты: документирование и практическая справка

## Статус: ✅ Done

## Дата завершения: 2026-04-04

## Что сделано

### Задача 06: Ревью и актуализация ADR-002 ✅

Обновлён `docs/adr/adr-002-orm-migrations-tests.md`:
- Добавлены пункты 5–7 в секцию «Решение»: UUID PK, StrEnum+native_enum, asyncio_mode
- Уточнён пункт об изоляции тестов: SQLite+aiosqlite явно обозначена как временная; ссылка на PostgreSQL harness исправлена (итерация 5, задача 13)
- Обновлена дата ADR: 2026-04-04
- Добавлена ссылка на `docs/tech/db-guide.md`

### Задача 07: Практическая справка `docs/tech/db-guide.md` ✅

Создан `docs/tech/db-guide.md` с:
- Деревом структуры слоя данных и таблицей ответственности модулей
- Полным набором alembic-команд (create / apply / rollback / current / history)
- Паттерном репозиториев (модульные функции, flush в репозитории, commit в сервисе)
- Примером инжекции сессии через `Annotated[AsyncSession, Depends(get_session)]`
- 5 SQL-сниппетами для разработчика

## Ключевые уточнения, выявленные при реализации

| Аспект | Выявлено |
|--------|---------|
| Паттерн репозиториев | Используются модульные функции, а не классы |
| Транзакции | `flush()` в репозитории, `commit()` в сервисе — явная граница транзакции |
| asyncio_mode | Конфигурируется в корневом `pyproject.toml`, применяется ко всему workspace |

## Проверка итерации

- ✅ `docs/tech/db-guide.md` создан; содержит 4 раздела + 5 SQL-сниппетов
- ✅ ADR-002 явно упоминает UUID PK, StrEnum, asyncio_mode, SQLite-изоляцию
- ✅ Все make-команды в справке: существующие без оговорок; будущие (итерация 4) — явно помечены

## Инфраструктурные фиксы (вне scope задач, выявлены при проверке DoD)

При прогоне `make backend-db-migrate` на реальном PostgreSQL обнаружены и исправлены два бага:

### 1. `backend/alembic/env.py` — Alembic не читал `.env`

`env.py` использует `os.environ.get("DATABASE_URL")` напрямую; `uv run` не загружает `.env` автоматически.

**Фикс:** добавлен `load_dotenv()` в начало файла (транзитивная зависимость `pydantic-settings`).

### 2. `backend/alembic/versions/0001_initial_schema.py` — двойное создание enum-типов

**Причина:** один и тот же объект `postgresql.ENUM(..., create_type=True)` использовался и для явного `enum.create(bind, checkfirst=True)`, и как тип колонки в `op.create_table()`. SQLAlchemy при создании таблицы повторно вызывает `create()` через DDL-event — уже с `checkfirst=False` — что приводит к `DuplicateObjectError`.

**Фикс:** для явного создания используются анонимные экземпляры `ENUM` с `checkfirst=True`; для колонок в `create_table` — отдельные экземпляры с `create_type=False`.

```python
# явное создание — идемпотентно
postgresql.ENUM("student", "teacher", name="user_role").create(bind, checkfirst=True)

# определение колонки — без повторного создания
user_role = postgresql.ENUM("student", "teacher", name="user_role", create_type=False)
```

## Артефакты

| Файл | Действие |
|------|----------|
| `docs/adr/adr-002-orm-migrations-tests.md` | обновлён |
| `docs/tech/db-guide.md` | создан |
| `backend/alembic/env.py` | добавлен `load_dotenv()` |
| `backend/alembic/versions/0001_initial_schema.py` | исправлен баг двойного создания enum-типов |
| `docs/tasks/impl/database/iteration-3-db-tooling/plan.md` | создан |
| `docs/tasks/impl/database/iteration-3-db-tooling/tasks/task-06-adr-review/plan.md` | создан |
| `docs/tasks/impl/database/iteration-3-db-tooling/tasks/task-06-adr-review/summary.md` | создан |
| `docs/tasks/impl/database/iteration-3-db-tooling/tasks/task-07-db-guide/plan.md` | создан |
| `docs/tasks/impl/database/iteration-3-db-tooling/tasks/task-07-db-guide/summary.md` | создан |
