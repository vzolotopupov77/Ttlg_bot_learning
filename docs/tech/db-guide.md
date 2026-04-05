# Практическая справка по работе с БД

Документ описывает, как устроен слой данных в проекте, как создавать и применять миграции, как писать репозитории и инжектировать сессию в FastAPI. Не дублирует [ADR-002](../adr/adr-002-orm-migrations-tests.md) — объясняет «как делать» на практике.

---

## 1. Структура слоя данных

```
backend/
  alembic.ini                          # конфиг Alembic (путь к env.py, URL переопределяется через env)
  alembic/
    env.py                             # async-runner миграций; читает DATABASE_URL из config
    versions/
      0001_initial_schema.py           # начальная ревизия
  src/ttlg_backend/
    storage/
      models.py                        # ORM-модели и StrEnum-перечисления
      repositories/
        users.py                       # CRUD для users
        lessons.py                     # CRUD для lessons
        assignments.py                 # CRUD для assignments
        dialogues.py                   # CRUD для dialogues / messages
        progress_summary.py            # CRUD для progress
    db.py                              # движок, фабрика сессий, get_session
    dependencies.py                    # FastAPI-зависимости (auth placeholder)
```

### Ключевые модули

| Файл | Ответственность |
|------|----------------|
| `storage/models.py` | ORM-модели (`User`, `Lesson`, `Assignment`, `Progress`, `Dialogue`, `Message`) и enum-перечисления (`UserRole`, `LessonStatus`, …) |
| `storage/repositories/*.py` | Тонкий слой доступа к данным: модульные async-функции, принимают `AsyncSession` первым аргументом |
| `db.py` | `init_db` — создаёт движок; `get_session` — async generator для `Depends`; `ping_db` — health-check |
| `dependencies.py` | Заглушка auth; `Depends(get_session)` подключается напрямую из `db.py` |

---

## 2. Миграции

### Makefile-цели

```bash
make backend-db-up       # docker compose up -d db              — поднять контейнер PostgreSQL
make backend-db-migrate  # alembic upgrade head                  — применить все ревизии
make backend-db-reset    # down -v → up --wait → migrate         — чистый старт с нуля
make backend-db-shell    # psql -U ttlg -d ttlg                  — интерактивный шелл
make backend-db-logs     # docker compose logs -f db             — логи контейнера
make backend-db-seed     # python backend/scripts/seed.py        — наполнить тестовыми данными
```

`backend-db-reset` останавливает контейнер, удаляет volume `ttlg_pg_data`, поднимает PostgreSQL заново (ожидая healthcheck) и сразу накатывает все миграции.

### Прямые команды через uv

Все alembic-команды запускаются из корня репозитория с явным указанием `alembic.ini`:

```bash
# создать новую ревизию с автогенерацией по моделям
uv run --package ttlg-backend alembic -c backend/alembic.ini revision --autogenerate -m "add_topic_table"

# проверить сгенерированный файл перед применением
# backend/alembic/versions/<rev>_add_topic_table.py

# применить все ревизии
uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

# откатить последнюю ревизию
uv run --package ttlg-backend alembic -c backend/alembic.ini downgrade -1

# посмотреть текущую версию в БД
uv run --package ttlg-backend alembic -c backend/alembic.ini current

# история ревизий
uv run --package ttlg-backend alembic -c backend/alembic.ini history --verbose
```

### Правило: модель + ревизия меняются в паре

При изменении `storage/models.py` — сразу создать и проверить ревизию. Коммитить оба файла вместе.

### Важно: шаблон ревизии

`backend/alembic/script.py.mako` содержит переменные `revision`, `down_revision` и т.д. — они обязательны для работы Alembic. Не удалять из шаблона.

---

## 3. Репозитории

### Паттерн

Репозитории реализованы как **модульные async-функции** (не классы): каждая функция принимает `AsyncSession` первым аргументом.

- `session.add(obj)` + `await session.flush()` — записать в транзакцию без коммита
- `await session.get(Model, id)` — получить по PK; возвращает `None` если не найдено
- `result.scalar_one_or_none()` — для запросов с `select`
- **Коммит — на уровне сервиса**, не репозитория

### Типовой шаблон нового репозитория

```python
"""SomeEntity persistence helpers."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ttlg_backend.storage.models import SomeEntity


async def create_some_entity(
    session: AsyncSession,
    *,
    field_a: str,
    field_b: int,
) -> SomeEntity:
    obj = SomeEntity(field_a=field_a, field_b=field_b)
    session.add(obj)
    await session.flush()
    return obj


async def get_some_entity_by_id(session: AsyncSession, entity_id: UUID) -> SomeEntity | None:
    return await session.get(SomeEntity, entity_id)


async def list_some_entities(session: AsyncSession) -> list[SomeEntity]:
    result = await session.execute(select(SomeEntity))
    return list(result.scalars().all())
```

### Итоги ревью (задача 12, итерация 5)

Все 5 репозиториев проверены по чек-листу:

| Репозиторий | None-handling | scalars() | Нет утечки сессии | DI через Depends | Итог |
|-------------|--------------|-----------|-------------------|-----------------|------|
| `users.py` | ✅ `session.get()` → None | ✅ `scalar_one_or_none()` | ✅ | ✅ | OK |
| `dialogues.py` | ✅ `scalar_one_or_none()` | ✅ `scalars().all()` для списка | ✅ | ✅ | OK |
| `lessons.py` | ✅ `session.get()` → None | ✅ `scalars().all()` для списка | ✅ | ✅ | OK |
| `assignments.py` | ✅ `session.get()` → None | ✅ `scalars().all()` для списка | ✅ | ✅ | OK |
| `progress_summary.py` | n/a (агрегация) | ✅ `scalar_one()` для COUNT | ✅ | ✅ | OK |

Паттерн class-based Repository (из skill `fastapi-templates`) **отклонён**: проект использует модульные async-функции — проще, достаточно для MVP, не требует абстракции.

### Реальный пример — `users.py`

```python
async def create_user(session, *, name, role, telegram_id=None) -> User:
    user = User(name=name, role=role, telegram_id=telegram_id)
    session.add(user)
    await session.flush()
    return user

async def get_user_by_id(session, user_id: UUID) -> User | None:
    return await session.get(User, user_id)

async def get_student_by_telegram_id(session, telegram_id: int) -> User | None:
    stmt = select(User).where(User.telegram_id == telegram_id, User.role == UserRole.student)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
```

---

## 4. Сессия в FastAPI

### Инжекция через Depends

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ttlg_backend.db import get_session
from ttlg_backend.storage.repositories import users as users_repo

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    user = await users_repo.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user
```

### Цикл жизни сессии

```
HTTP Request
  │
  ├─ get_session() открывает async_sessionmaker сессию
  │
  ├─ endpoint выполняется: репозитории делают flush()
  │
  ├─ сервис вызывает await session.commit()  ← явно
  │
  └─ get_session() закрывает сессию
       └─ при исключении — автоматический rollback
```

**Ключевые детали:**
- `get_session` — async generator; при исключении автоматически вызывает `session.rollback()`
- `async_sessionmaker` создан с `expire_on_commit=False` — объекты доступны после `commit`
- `session.flush()` в репозиториях — записывает в транзакцию без коммита (FK-проверки выполняются сразу)
- `session.commit()` — в сервисном слое, после завершения всей операции

---

## 5. SQL-сниппеты

Для выполнения через `make backend-db-shell` или через `psql` напрямую. Проверены на seed-данных (`make backend-db-seed`).

### 5.1. Все пользователи с ролями

```sql
-- список всех пользователей системы
SELECT id, name, role, telegram_id, created_at
FROM users
ORDER BY role, name;
```

### 5.2. Занятия конкретного ученика

```sql
-- занятия ученика с именем преподавателя и статусом
SELECT l.id,
       l.topic,
       l.scheduled_at,
       l.status,
       t.name AS teacher_name
FROM lessons l
JOIN users t ON t.id = l.teacher_id
WHERE l.student_id = '<student-uuid>'
ORDER BY l.scheduled_at DESC
LIMIT 20;
```

### 5.3. ДЗ с истёкшим дедлайном

```sql
-- задания, у которых статус overdue или дедлайн уже прошёл
SELECT a.id,
       a.description,
       a.due_date,
       a.status,
       u.name AS student_name
FROM assignments a
JOIN users u ON u.id = a.student_id
WHERE a.status = 'overdue'
   OR (a.due_date < current_date AND a.status = 'pending')
ORDER BY a.due_date;
```

### 5.4. Последние 10 сообщений в диалогах

```sql
-- последние сообщения по всем диалогам с именем ученика
SELECT m.id,
       m.role,
       left(m.content, 80) AS content_preview,
       m.created_at,
       u.name AS student_name
FROM messages m
JOIN dialogues d ON d.id = m.dialogue_id
JOIN users u ON u.id = d.student_id
ORDER BY m.created_at DESC
LIMIT 10;
```

### 5.5. Прогресс по всем ученикам

```sql
-- агрегат прогресса с именами учеников
SELECT u.name AS student_name,
       p.period_start,
       p.period_end,
       p.lessons_completed,
       p.assignments_done,
       p.assignments_total,
       p.summary
FROM progress p
JOIN users u ON u.id = p.student_id
ORDER BY p.period_start DESC, u.name;
```

---

## 6. Просмотр данных

Открыть интерактивный шелл: `make backend-db-shell`

### Полезные `psql`-мета-команды

| Команда | Что делает |
|---------|-----------|
| `\dt` | Список всех таблиц в текущей схеме |
| `\d+ users` | Структура таблицы `users` с индексами и constraints |
| `\x` | Переключить расширенный (вертикальный) вывод строк |
| `\timing` | Включить/выключить отображение времени выполнения запроса |
| `\q` | Выйти из `psql` |

### Быстрая инспекция seed-данных

```sql
-- убедиться, что seed применён
SELECT name, role FROM users ORDER BY role;

-- посмотреть UUID seed-ученика (нужен для запросов ниже)
SELECT id FROM users WHERE telegram_id = 111111111;

-- занятия seed-ученика
SELECT topic, scheduled_at, status FROM lessons
WHERE student_id = (SELECT id FROM users WHERE telegram_id = 111111111);

-- задания seed-ученика
SELECT description, due_date, status FROM assignments
WHERE student_id = (SELECT id FROM users WHERE telegram_id = 111111111);
```

> `DEV_STUDENT_TELEGRAM_ID = 111111111` — фиксированный telegram_id тестового ученика из `backend/scripts/seed.py`.

---

## 7. Тесты с PostgreSQL

### Быстрый старт

```bash
make backend-db-up           # поднять контейнер PostgreSQL
make backend-db-test-create  # создать базу ttlg_test (однократно)
make backend-test            # запустить все тесты против PostgreSQL
```

### Конфигурация

`DATABASE_TEST_URL` — URL тестовой базы. По умолчанию: `postgresql+asyncpg://ttlg:ttlg@127.0.0.1:5432/ttlg_test`.

Задать через переменную окружения или `.env`:
```
DATABASE_TEST_URL=postgresql+asyncpg://ttlg:ttlg@127.0.0.1:5432/ttlg_test
```

### Стратегия изоляции

Каждый тест получает чистую схему: `drop_all + create_all` при каждом вызове фикстуры `pg_session`. Это гарантирует полную изоляцию без зависимости от порядка тестов.

Примечание: session-scoped fixtures с `asyncio_default_fixture_loop_scope="function"` не поддерживаются asyncpg (event loop mismatch), поэтому используется function-scoped подход с drop/create.

### Структура фикстур (`backend/tests/conftest.py`)

| Фикстура | Scope | Назначение |
|----------|-------|-----------|
| `pg_session` | function | async engine → drop_all → create_all → session |
| `api_client_sqlite` | function | ASGI client с override `get_session` → `pg_session` |
| `dialogue_client` | function | ASGI client + mock LLM + pre-seeded student user |

### Добавить новый тест с PostgreSQL

```python
async def test_something(api_client_sqlite: AsyncClient) -> None:
    r = await api_client_sqlite.post("/v1/users", json={"name": "U", "role": "student"})
    assert r.status_code == 201
```

Если нужна прямая работа с сессией (без HTTP):
```python
async def test_repo(pg_session: AsyncSession) -> None:
    from ttlg_backend.storage.repositories import users as repo
    user = await repo.create_user(pg_session, name="U", role="student")
    await pg_session.commit()
    assert user.id is not None
```

---

## Связанные документы

- [docs/data-model.md](../data-model.md) — логическая и физическая схема БД
- [docs/adr/adr-002-orm-migrations-tests.md](../adr/adr-002-orm-migrations-tests.md) — решения по ORM, Alembic, тестам
- [docs/adr/adr-001-database.md](../adr/adr-001-database.md) — выбор PostgreSQL
