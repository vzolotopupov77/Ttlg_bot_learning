# ADR-002: ORM, миграции и тестовый раннер backend

| | |
|---|---|
| **Статус** | Принято |
| **Дата** | 2026-04-05 (обновлено: итерация 5, задача 13 завершена) |
| **Контекст** | Старт backend на FastAPI с PostgreSQL ([ADR-001](adr-001-database.md)); нужны персистентная схема, эволюция схемы и автоматизированные тесты API. |

---

## Контекст

Backend хранит доменные сущности в PostgreSQL и отдаёт HTTP API. Нужно:

- единый способ описания таблиц и связей в коде;
- воспроизводимые изменения схемы между окружениями;
- тесты, совместимые с **async**-стеком FastAPI и не ломающие изоляцию данных.

СУБД и sync-драйвер уже не рассматриваются — выбран async-путь под `asyncpg` ([ADR-001](adr-001-database.md)).

---

## Рассмотренные варианты

### 1. ORM: SQLAlchemy 2.x (async)

**Плюсы:**

- Стандарт для FastAPI + PostgreSQL; `AsyncSession`, декларативные модели, связи, типизация.
- Тесная интеграция с **Alembic** (те же метаданные/модели).
- Зрелая экосистема и документация.

**Минусы:**

- Больше концепций, чем у «тонкого» слоя над SQL.

**Вывод:** оптимальный баланс для растущего домена.

---

### 2. ORM: SQLModel

**Плюсы:**

- Объединение SQLAlchemy и Pydantic; меньше дублирования DTO в простых CRUD.

**Минусы:**

- Дополнительная абстракция и связка с версиями SQLAlchemy/Pydantic; для сложного домена часто всё равно нужны отдельные схемы API.
- Проект уже использует Pydantic в API отдельно — выгода не критична на старте.

**Вывод:** отложено; при необходимости пересмотреть после появления большого объёма CRUD.

---

### 3. Без ORM: только asyncpg (сырой SQL)

**Плюсы:**

- Минимум зависимостей; полный контроль над SQL.

**Минусы:**

- Ручное сопровождение маппинга, миграций на уровне SQL без единой модели в коде; выше риск расхождения схемы и кода.

**Вывод:** не выбираем на текущем этапе; возможен точечный raw-SQL внутри репозиториев при необходимости.

---

### 4. Миграции: Alembic

**Плюсы:**

- Де-факто стандарт для SQLAlchemy; автогенерация по метаданным моделей; версионирование ревизий.

**Минусы:**

- Настройка `env.py` под async — одноразовая работа.

**Вывод:** использовать Alembic; каталог ревизий в репозитории (например `backend/alembic/` — конкретный путь задаётся в задаче каркаса).

---

### 5. Тесты: Starlette `TestClient` (sync)

**Плюсы:**

- Простой старт; встроен в Starlette/FastAPI-документацию.

**Минусы:**

- Запускает async-код в event loop внутри sync-обёртки; при сложных async-фикстурах и чистом async-тестовом коде возможны предупреждения и менее предсказуемое поведение.

**Вывод:** не основной выбор для «все async» пайплайна.

---

### 6. Тесты: `httpx.AsyncClient` + `pytest-asyncio`

**Плюсы:**

- Нативный async end-to-end вызов приложения; согласуется с `async` фикстурами и `AsyncSession` в тестах.

**Минусы:**

- Чуть больше бойлерплейта в фикстурах (жизненный цикл приложения, клиент).

**Вывод:** основной способ smoke/API-тестов backend.

---

## Решение

1. **ORM:** **SQLAlchemy 2.x** в async-режиме (`AsyncSession`, `asyncpg`).
2. **Миграции:** **Alembic**, ревизии в репо; `DATABASE_URL` async-формата `postgresql+asyncpg://...` ([ADR-001](adr-001-database.md)).
3. **Тесты:** **pytest**, **pytest-asyncio**, **httpx** (`AsyncClient`) для вызова ASGI-приложения.
4. **Изоляция БД в тестах:** отдельная база `ttlg_test` в Docker-контейнере PostgreSQL; `drop_all + create_all` per test (function-scoped фикстуры). Реализовано в **итерации 5 (задача 13)**. `TTLG_ALLOW_SQLITE_TEST` снят из `backend/tests/`; `make backend-test` работает без SQLite-заглушки. Bot-тесты (`tests/`) используют SQLite временно — миграция запланирована отдельно.
5. **UUID PK:** все таблицы используют `Uuid(as_uuid=True)` + `default=uuid.uuid4` — генерация на стороне Python, не автоинкремент.
6. **StrEnum + native PostgreSQL enum:** `StrEnum` (Python 3.11+) + `SQLEnum(native_enum=True, values_callable=lambda e: [i.value for i in e])` — единый паттерн для всех enum-полей; создаёт именованные типы в PostgreSQL (`user_role`, `lesson_status`, и т.д.).
7. **pytest-asyncio:** `asyncio_mode = "auto"` + `asyncio_default_fixture_loop_scope = "function"` в корневом `pyproject.toml`; распространяется на backend-тесты через uv workspace.

---

## Последствия

- В `pyproject.toml` (workspace uv) зависимости `sqlalchemy[asyncio]`, `asyncpg`, `alembic` — в `[project.dependencies]` backend; `pytest`, `pytest-asyncio`, `httpx`, `respx` — в `[dependency-groups] dev` backend; `aiosqlite` — в dev root (bot-тесты). Backend-тесты `aiosqlite` не требуют.
- Разработчики поддерживают модели в `storage/` и ревизии Alembic в паре с изменениями схемы.
- Документ [docs/data-model.md](../data-model.md) остаётся источником доменной схемы; расхождения моделей и документа устраняются в задачах ORM/миграций с явной записью в summary задачи.
- `make backend-test` работает без `TTLG_ALLOW_SQLITE_TEST`; требует запущенного контейнера PostgreSQL и базы `ttlg_test` (`make backend-db-up && make backend-db-test-create`).
- Практическая справка по работе с БД: [docs/tech/db-guide.md](../tech/db-guide.md).
