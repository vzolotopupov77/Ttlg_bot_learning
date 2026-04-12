# Задача 06 — Миграция: добавить преподавателя в БД: план

## Цель

Вставить запись преподавателя Владимира (`vzolotoy@mail.ru`) в таблицу `users` через отдельную Alembic-миграцию с bcrypt-хешем пароля; `.env.example` актуализирован; `POST /v1/auth/login` с данными преподавателя возвращает `200`.

## Предусловие

- Задача 04 завершена: `users.password_hash` существует, роутер `POST /v1/auth/login` реализован
- Задача 05 завершена (порядок не критичен, но выполнять после неё для корректной цепочки миграций)

## Входные данные

| Файл | Роль |
|------|------|
| `.env.example` | Актуализировать: добавить `TEACHER_DEFAULT_PASSWORD` |
| `backend/alembic/versions/` | Цепочка миграций |
| `backend/src/ttlg_backend/storage/models.py` | ORM User с полем `password_hash` |

## Детали реализации

### Переменная окружения

В `.env.example` добавить:
```dotenv
# Пароль по умолчанию для преподавателя (только для dev; в prod — задать своё значение)
TEACHER_DEFAULT_PASSWORD=changeme_teacher
```

**Правило (sharp-edges):** Пароль не хранится в открытом виде в коде или git. В миграции хешировать на лету через `passlib`; если `TEACHER_DEFAULT_PASSWORD` не задан — использовать фиксированный dev-дефолт с предупреждением в логе.

### Имя файла миграции

```
backend/alembic/versions/2026_04_12_009_seed_teacher.py
```

### Структура миграции

```python
"""Seed teacher user (Владимир / vzolotoy@mail.ru)."""

import os
import uuid
from passlib.hash import bcrypt

revision = "..."
down_revision = "..."  # миграция seed_mock_data из задачи 05

TEACHER_ID = "00000000-0000-0000-0000-000000000001"  # фиксированный UUID

def upgrade() -> None:
    password = os.getenv("TEACHER_DEFAULT_PASSWORD", "changeme_teacher")
    password_hash = bcrypt.hash(password)

    op.execute(f"""
        INSERT INTO users (id, role, name, email, password_hash, created_at)
        VALUES (
            '{TEACHER_ID}',
            'teacher',
            'Владимир',
            'vzolotoy@mail.ru',
            '{password_hash}',
            now()
        )
        ON CONFLICT (id) DO NOTHING;
    """)

def downgrade() -> None:
    op.execute(f"DELETE FROM users WHERE id = '{TEACHER_ID}';")
```

> `ON CONFLICT DO NOTHING` — защита от повторного применения в dev-среде.
> Фиксированный UUID `TEACHER_ID` гарантирует детерминированный `downgrade`.

### Связь с auth-роутером

После применения миграции:

```bash
POST /v1/auth/login
{
  "email": "vzolotoy@mail.ru",
  "password": "<TEACHER_DEFAULT_PASSWORD>",
  "role": "teacher"
}
→ 200 {"user": {"id": "...", "name": "Владимир", "role": "teacher"}}
  + httpOnly cookie с JWT
```

### Обновление `.env.example`

Полный список новых переменных, добавленных в итерации 1:

```dotenv
# JWT
SECRET_KEY=changeme_secret_key_min_32_chars
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Seed (только dev)
TEACHER_DEFAULT_PASSWORD=changeme_teacher
```

## Порядок применения всех миграций итерации 1

```
0001_initial_schema
    ↓
a3f8c91d2b04_user_profile_lesson_duration
    ↓
5dcbe7dd0861_schema_review_fixes
    ↓  (Задача 03/04)
2026_04_12_004_add_lesson_flags
    ↓
2026_04_12_005_add_user_auth_fields
    ↓
2026_04_12_006_add_reschedule_requests
    ↓
2026_04_12_007_add_system_settings
    ↓  (Задача 05)
2026_04_12_008_seed_mock_data
    ↓  (Задача 06)
2026_04_12_009_seed_teacher
```

## Makefile-цели

Убедиться, что в `Makefile` есть (или добавить):
```makefile
backend-migrate:
    cd backend && uv run alembic upgrade head
```

## Артефакты

- `backend/alembic/versions/2026_04_12_009_seed_teacher.py`
- `.env.example` — добавлены `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `TEACHER_DEFAULT_PASSWORD`
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-06-teacher-migration/plan.md` (этот файл)
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-06-teacher-migration/summary.md` — после выполнения

## Definition of Done

**Агент:**

- [ ] Миграция применяется без ошибок: `alembic upgrade head`
- [ ] `POST /v1/auth/login` с `email=vzolotoy@mail.ru` и паролем из `.env` → `200` + JWT-cookie
- [ ] `.env.example` содержит `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `TEACHER_DEFAULT_PASSWORD`
- [ ] Пароль не хранится в открытом виде в коде — только bcrypt-хеш в миграции
- [ ] `downgrade()` удаляет только запись преподавателя, не ломает схему

**Пользователь:**

- [ ] `make backend-migrate` — миграция прошла без ошибок
- [ ] В Swagger `POST /v1/auth/login` с `vzolotoy@mail.ru` → получен JWT
