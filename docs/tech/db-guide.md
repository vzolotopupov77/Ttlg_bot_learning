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

### Существующие Makefile-цели

```bash
make backend-db-up       # docker compose up -d db  — поднять контейнер PostgreSQL
make backend-db-migrate  # alembic upgrade head      — применить все ревизии
```

> **Итерация 4 (задача 08)** добавит: `backend-db-reset`, `backend-db-shell`, `backend-db-logs`.

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

Для выполнения через `make backend-db-shell` (добавляется в итерации 4) или через `psql` напрямую.

> Верификация на seed-данных — задача 10, итерация 4.

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

## Связанные документы

- [docs/data-model.md](../data-model.md) — логическая и физическая схема БД
- [docs/adr/adr-002-orm-migrations-tests.md](../adr/adr-002-orm-migrations-tests.md) — решения по ORM, Alembic, тестам
- [docs/adr/adr-001-database.md](../adr/adr-001-database.md) — выбор PostgreSQL
