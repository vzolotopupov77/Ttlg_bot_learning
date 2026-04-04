# Итерация 3 — Инструменты: документирование и практическая справка

## Мета

| | |
|---|---|
| **Область** | database |
| **Итерация** | 3 |
| **Статус** | 🚧 In Progress |
| **Дата начала** | 2026-04-04 |

## Цель

Убедиться, что ADR-002 отражает фактически принятые решения в коде, и создать практическую справку `docs/tech/db-guide.md` — единую точку входа по работе с БД для агентов и разработчиков.

## Ценность

После итерации любой участник может без поиска по коду понять, как добавить таблицу, создать миграцию, написать репозиторий и разобраться в текущем тестовом окружении.

## Артефакты

| Артефакт | Действие |
|----------|----------|
| `docs/adr/adr-002-orm-migrations-tests.md` | обновить (задача 06) |
| `docs/tech/db-guide.md` | создать (задача 07) |

## Состав работ

### Задача 06: Ревью и актуализация ADR-002

Сверить ADR-002 с реализацией (`storage/models.py`, `backend/alembic/`, `pyproject.toml`) и зафиксировать решения, принятые в ходе реализации, которые отсутствуют в ADR:

- UUID PK во всех таблицах (`Uuid(as_uuid=True)` + `default=uuid.uuid4`)
- `StrEnum` + `SQLEnum(native_enum=True, values_callable=...)` — паттерн PostgreSQL enum-типов
- `asyncio_mode = "auto"` в корневом `pyproject.toml`
- Текущая изоляция тестов — SQLite+aiosqlite (`TTLG_ALLOW_SQLITE_TEST=1`) — временное решение до итерации 5, задача 13

Исправить устаревшую ссылку: «задача 08 tasklist» → «итерация 5, задача 13».

### Задача 07: Практическая справка `docs/tech/db-guide.md`

Создать новый файл с 4 разделами:
1. Структура слоя данных (`models.py`, `repositories/`, `db.py`, `dependencies.py`)
2. Миграции (create / apply / rollback; make-цели; alembic.ini)
3. Репозитории (паттерн, типовой шаблон нового репозитория)
4. Сессия в FastAPI (`Depends(get_session)`, цикл жизни)

Плюс 5 SQL-сниппетов для работы через `psql` (верификация — в итерации 4, задача 10).

## Контекст реализации

**Текущее состояние кода:**
- `storage/models.py` — UUID PK, StrEnum + native_enum=True, DateTime(timezone=True), FK с каскадами и index=True
- `alembic/` — ревизия `0001_initial_schema.py`; `env.py` настроен под async
- `db.py` — `create_async_engine` / `async_sessionmaker` / `get_session` (async generator)
- Тесты — SQLite+aiosqlite через `TTLG_ALLOW_SQLITE_TEST=1`; `asyncio_mode = "auto"` в корневом `pyproject.toml`

**Существующие Makefile-цели по БД:**
- `backend-db-up` — поднять контейнер
- `backend-db-migrate` — применить миграции
- `backend-test` — запустить тесты

**Отсутствуют (добавляются в итерации 4):** `backend-db-shell`, `backend-db-reset`, `backend-db-logs`, `backend-db-seed`

## Проверка итерации

**Агент:**
- `docs/tech/db-guide.md` существует; содержит 4 раздела + 5 SQL-сниппетов
- ADR-002 явно упоминает UUID PK, StrEnum+native_enum, asyncio_mode, SQLite-изоляцию как временную
- Все make-команды в справке существуют в Makefile или явно помечены как «итерация 4»

**Пользователь:** открыть `docs/tech/db-guide.md` → раздел «Миграции» → выполнить `alembic revision --autogenerate -m "test"` → убедиться, что файл создан → `alembic downgrade -1` → удалить файл — без обращения к другим документам.
