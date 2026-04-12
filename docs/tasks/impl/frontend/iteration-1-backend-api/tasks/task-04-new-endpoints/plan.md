# Задача 04 — Новые endpoints backend: план

## Цель

Реализовать все endpoints из API-контрактов Итерации 0 в `backend/src/ttlg_backend/`; применить Alembic-миграции для новых таблиц и полей (из Задачи 03); написать smoke-тесты.

## Предусловие

Задача 03 завершена: `docs/data-model.md` обновлён, ORM-модели расширены.

## Входные данные

| Файл | Роль |
|------|------|
| [docs/tech/api-contracts.md](../../../../../tech/api-contracts.md) | Контракты всех endpoints |
| [docs/api-conventions.md](../../../../../api-conventions.md) | Формат ошибок, пагинация |
| [backend/src/ttlg_backend/storage/models.py](../../../../../../backend/src/ttlg_backend/storage/models.py) | ORM-модели (расширены в задаче 03) |
| [backend/src/ttlg_backend/config.py](../../../../../../backend/src/ttlg_backend/config.py) | Настройки приложения |

## Шаг 1: Зависимости

```bash
uv add passlib[bcrypt] python-jose[cryptography]
uv add --group dev pytest-asyncio httpx
```

## Шаг 2: Конфигурация

Расширить `backend/src/ttlg_backend/config.py`:

```python
secret_key: str = Field(..., min_length=1, description="JWT secret key")
access_token_expire_minutes: int = Field(default=60, gt=0)
```

- `secret_key` — обязательное, `ValidationError` при пустой строке или отсутствии (`sharp-edges`)
- `access_token_expire_minutes > 0` — `gt=0` в Field или `field_validator`
- Добавить в `.env.example`: `SECRET_KEY=changeme`, `ACCESS_TOKEN_EXPIRE_MINUTES=60`

## Шаг 3: Alembic-миграции (DDL)

Создать 4 миграции (из Задачи 03) и применить:

```bash
alembic revision --autogenerate -m "add_lesson_flags"
alembic revision --autogenerate -m "add_user_auth_fields"
alembic revision --autogenerate -m "add_reschedule_requests"
alembic revision --autogenerate -m "add_system_settings"
alembic upgrade head
```

> Проверить сгенерированные миграции перед применением — autogenerate может не улавливать CHECK-constraints и индексы; дописать вручную при необходимости.

## Шаг 4: Общие зависимости — `api/deps.py`

Новый файл `backend/src/ttlg_backend/api/deps.py`:

```python
ALGORITHM = "HS256"  # константа, не из конфига, не из заголовка токена

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
    settings: Settings = Depends(get_settings),
) -> User:
    # jose.jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    # — явный список алгоритмов, никогда не читать из токена
    ...
```

Роль-зависимости:
- `require_teacher` — проверяет `current_user.role == "teacher"`, иначе `403`
- `require_student` — проверяет `current_user.role == "student"`, иначе `403`

## Шаг 5: Auth-роутер — `api/auth.py`

**Endpoints:**

| Метод | Путь | Код | Описание |
|-------|------|-----|---------|
| POST | `/v1/auth/login` | 200 | Вход: email + password + role → JWT в cookie |
| POST | `/v1/auth/logout` | 204 | Очистка httpOnly cookie |
| GET | `/v1/auth/me` | 200 | Текущий пользователь |

**Сервис** `services/auth_service.py`:
```python
ALGORITHM = "HS256"  # только здесь; deps.py импортирует отсюда

def hash_password(plain: str) -> str: ...
def verify_password(plain: str, hashed: str | None) -> bool:
    # hashed должен быть непустым; иначе — False, не bcrypt-compare
    if not hashed:
        return False
    return bcrypt.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta) -> str: ...
def decode_token(token: str, secret_key: str) -> dict:
    return jwt.decode(token, secret_key, algorithms=["HS256"])
    # algorithms= явно, не алгоритм из заголовка токена
```

**Безопасность (sharp-edges):**
- JWT-алгоритм — `ALGORITHM = "HS256"` — константа в `auth_service.py`; при decode `algorithms=["HS256"]`
- `verify_password` — возвращает `False` при `hashed is None` или `hashed == ""`
- Токен помещается в `httpOnly` cookie; в JSON ответа `200` — только данные пользователя

## Шаг 6: Teacher-роутер — `api/teacher.py`

Все endpoints — `Depends(require_teacher)`.

| Метод | Путь | Параметры | Описание |
|-------|------|-----------|---------|
| GET | `/v1/teacher/schedule` | `week_start: date` | Занятия недели |
| GET | `/v1/teacher/bot-requests` | `limit: int = 10` | Последние N сообщений учеников |
| GET | `/v1/teacher/unconfirmed-lessons` | `days: int = 2` | Неподтверждённые занятия |
| GET | `/v1/teacher/pending-homework` | `days: int = 2` | Занятия с несданным ДЗ |
| POST | `/v1/teacher/remind-unconfirmed` | — | Напомнить; ответ `{"notified_count": N}` |
| POST | `/v1/teacher/remind-pending-homework` | — | Напомнить; ответ `{"notified_count": N}` |
| GET | `/v1/teacher/reschedule-requests` | — | Запросы на перенос |
| PATCH | `/v1/teacher/reschedule-requests/{request_id}` | body: `{"status": "accepted"\|"rejected"}` | Принять/отклонить |

**Сервис** `services/teacher_service.py`:
- Запросы через `storage/repositories/teacher.py`
- `get_weekly_schedule(session, teacher_id, week_start)` → список занятий с флагами и именем ученика
- `get_bot_requests(session, limit)` → последние N сообщений из `messages` где `role=user`
- `get_unconfirmed_lessons(session, teacher_id, days)` → занятия с `confirmed_by_student=false` в ближайшие N дней
- `get_pending_homework(session, teacher_id, days)` → занятия с `homework_sent=true, solution_received=false` за N дней
- Напоминания: заглушка (stub) — логирование + счёт записей; реальная отправка через бот — будущая итерация

**Репозиторий** `storage/repositories/teacher.py`:
- Async SQLAlchemy queries с `select()`, `join()`, `where()`
- Индексы `scheduled_at`, `student_id` обеспечивают производительность

## Шаг 7: Students-роутер — `api/students.py`

Все endpoints — `Depends(require_teacher)`.

| Метод | Путь | Код | Описание |
|-------|------|-----|---------|
| GET | `/v1/students` | 200 | Список (`limit`, `offset`) — пагинация |
| POST | `/v1/students` | 201 | Создать ученика (`role=student`) |
| GET | `/v1/students/{id}` | 200/404 | Профиль |
| PUT | `/v1/students/{id}` | 200/404 | Обновить профиль |
| DELETE | `/v1/students/{id}` | 204/404 | Удалить |
| GET | `/v1/students/{id}/lessons` | 200/404 | История занятий |
| GET | `/v1/students/{id}/dialogue` | 200/404 | Сообщения диалога |
| GET | `/v1/students/{id}/stats` | 200/404 | Агрегаты (счётчики) |

**Тело `POST/PUT`:**
```json
{
  "name": "string",
  "class_label": "string|null",
  "phone": "string|null",
  "email": "string|null",
  "notes": "string|null"
}
```

`telegram_id` не принимается с формы преподавателя.

**Конфликт при создании:** если `email` уже занят → `409` `conflict`.

**Сервис** `services/students_service.py`.

**Диалог:** `GET /{id}/dialogue?limit&offset` — сортировка от новых к старым (удобно для scroll).

## Шаг 8: Settings-роутер — `api/settings.py`

Только `Depends(require_teacher)`.

| Метод | Путь | Код | Описание |
|-------|------|-----|---------|
| GET | `/v1/settings` | 200 | Текущие настройки |
| PUT | `/v1/settings` | 200 | Сохранить |

**Схема:**
```json
{
  "teacher_name": "string",
  "default_lesson_duration_minutes": 60,
  "lesson_reminder_hours_before": 24,
  "homework_reminder_hours_before": 48
}
```

Хранение — таблица `system_settings` (key-value). Сервис `services/settings_service.py` читает/записывает именованные ключи.

## Шаг 9: Student schedule — `api/student_schedule.py`

Только `Depends(require_student)`.

| Метод | Путь | Параметры | Описание |
|-------|------|-----------|---------|
| GET | `/v1/student/schedule` | `week_start: date` | Расписание текущего ученика |

Возвращает только занятия `current_user` (без чужих данных).

## Шаг 10: Расширение `api/lessons.py`

Добавить к существующим `POST`, `GET /{id}`, `PATCH /{id}/status`:

| Метод | Путь | Код | Описание |
|-------|------|-----|---------|
| PUT | `/v1/lessons/{lesson_id}` | 200/404 | Полная замена полей |
| DELETE | `/v1/lessons/{lesson_id}` | 204/404 | Удалить занятие |
| PATCH | `/v1/lessons/{lesson_id}/flags` | 200/404 | Обновить флаги (частично) |

**`PATCH /flags` body** — только изменяемые bool-поля из набора 5 флагов.

## Шаг 11: Регистрация роутеров в `main.py`

```python
from ttlg_backend.api.auth import router as auth_router
from ttlg_backend.api.teacher import router as teacher_router
from ttlg_backend.api.students import router as students_router
from ttlg_backend.api.settings import router as settings_router
from ttlg_backend.api.student_schedule import router as student_schedule_router

app.include_router(auth_router, prefix="/v1")
app.include_router(teacher_router, prefix="/v1")
app.include_router(students_router, prefix="/v1")
app.include_router(settings_router, prefix="/v1")
app.include_router(student_schedule_router, prefix="/v1")
```

## Шаг 12: Smoke-тесты — `backend/tests/`

Файлы:
- `tests/test_auth.py` — POST /v1/auth/login (200 с корректными данными, 401 с неверными, 401 без токена к /me)
- `tests/test_teacher.py` — GET /v1/teacher/schedule (200 с токеном teacher, 401 без токена, 403 с токеном student)
- `tests/test_students.py` — GET /v1/students (200 + 401), POST /v1/students (201)
- `tests/test_settings.py` — GET /v1/settings (200 + 401)

Тесты используют `httpx.AsyncClient` + `pytest-asyncio`; БД — изолированная (aiosqlite или тестовый PostgreSQL — согласно ADR-002).

## Формат ошибок (api-conventions)

Все 4xx/5xx — единый формат:
```json
{"error": {"code": "...", "message": "..."}}
```

Нет `detail: str` в ответах (FastAPI default). Реализовать через `HTTPException` + кастомный `exception_handler` или `api_error()` (уже есть в `api/errors.py`).

## Структура файлов (итог)

```
backend/src/ttlg_backend/
├── api/
│   ├── auth.py           ← новый
│   ├── deps.py           ← новый
│   ├── teacher.py        ← новый
│   ├── students.py       ← новый
│   ├── settings.py       ← новый
│   ├── student_schedule.py ← новый
│   ├── lessons.py        ← расширен (PUT, DELETE, PATCH /flags)
│   └── ...existing...
├── services/
│   ├── auth_service.py   ← новый
│   ├── teacher_service.py ← новый
│   ├── students_service.py ← новый
│   ├── settings_service.py ← новый
│   └── ...existing...
├── storage/repositories/
│   ├── teacher.py        ← новый
│   ├── settings.py       ← новый
│   └── ...existing...
backend/tests/
├── test_auth.py          ← новый
├── test_teacher.py       ← новый
├── test_students.py      ← новый
└── test_settings.py      ← новый
backend/alembic/versions/
├── ...existing 3 миграции...
├── 2026_04_12_004_add_lesson_flags.py
├── 2026_04_12_005_add_user_auth_fields.py
├── 2026_04_12_006_add_reschedule_requests.py
└── 2026_04_12_007_add_system_settings.py
```

## Артефакты

- `backend/src/ttlg_backend/api/` — 6 файлов (4 новых + deps.py + lessons расширен)
- `backend/src/ttlg_backend/services/` — 4 новых сервиса
- `backend/src/ttlg_backend/storage/repositories/` — 2 новых репозитория
- `backend/src/ttlg_backend/config.py` — расширен
- `backend/src/ttlg_backend/main.py` — расширен
- `backend/alembic/versions/` — 4 DDL-миграции
- `backend/tests/` — 4 файла smoke-тестов
- `.env.example` — добавлены `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `docs/tech/api-contracts.md` — обновить при отклонениях от проекта

## Definition of Done

**Агент:**

- [ ] Все endpoints из Итерации 0 реализованы и доступны в OpenAPI `/docs`
- [ ] Каждый роутер имеет `response_model=` — нет «голых» endpoints
- [ ] Единый формат ошибок — нет `detail: str` в ответах 4xx/5xx
- [ ] List-endpoints возвращают пагинированный результат (`items`, `total`, `limit`, `offset`)
- [ ] Миграции применяются без ошибок: `alembic upgrade head`
- [ ] `make backend-test` — все smoke-тесты зелёные
- [ ] JWT-защита: без токена → `401`; роль не совпадает → `403`
- [ ] JWT-алгоритм зафиксирован: `algorithms=["HS256"]` явно при декодировании
- [ ] `SECRET_KEY=""` при старте поднимает `ValidationError`
- [ ] `verify_password` не возвращает `True` при пустом/None хеше
- [ ] `docs/tech/api-contracts.md` соответствует реализации

**Пользователь:**

- [ ] `make backend-run` → `http://localhost:8000/docs` — видны разделы auth, teacher, students, settings
- [ ] `POST /v1/auth/login` с данными преподавателя → `200` + JWT
