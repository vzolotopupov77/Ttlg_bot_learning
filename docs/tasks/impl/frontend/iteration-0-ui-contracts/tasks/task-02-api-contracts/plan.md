# Задача 02 — API-контракты для frontend: план

## Цель

Спроектировать HTTP-контракты для всех новых endpoints, необходимых для отрисовки 5 экранов frontend. Дополнить `docs/tech/api-contracts.md` разделом «API для frontend».

---

## Контекст

Входные данные:
- `docs/spec/frontend-requirements.md` (результат Задачи 01) — экраны и данные, которые они отображают
- `docs/tech/api-contracts.md` — уже существующие MVP-контракты; дублирования избегать
- `docs/data-model.md` — схема данных, на которую опираются ответы API
- Skill `api-design-principles` — нейминг, коды, форматы ошибок, пагинация

Существующие MVP-маршруты (не дублировать):
- `POST /v1/users`, `GET /v1/users/{user_id}`, `GET /v1/users/{user_id}/progress`
- `POST /v1/lessons`, `GET /v1/lessons/{lesson_id}`, `PATCH /v1/lessons/{lesson_id}/status`
- `POST /v1/assignments`, `GET /v1/assignments/{assignment_id}`, `PATCH /v1/assignments/{assignment_id}/status`
- `POST /v1/dialogue/message`

---

## Новые маршруты по группам

### Аутентификация (`/v1/auth`)

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `POST` | `/v1/auth/login` | `200` | Вход по email + пароль; устанавливает httpOnly cookie с JWT |
| `POST` | `/v1/auth/logout` | `204` | Очистка cookie |
| `GET` | `/v1/auth/me` | `200` | Текущий пользователь (id, name, role) |

**Детали `POST /v1/auth/login`:**
- Request: `{ email: string, password: string }`
- Response `200`: `{ access_token: string, token_type: "bearer", user: { id: UUID, name: string, role: "teacher"|"student" } }`
- Ошибки: `401` `invalid_credentials`; `422` `validation_error`

**Детали `GET /v1/auth/me`:**
- Response `200`: `{ id: UUID, name: string, role: "teacher"|"student" }`
- Ошибки: `401` `unauthorized` (нет или невалидный токен)

---

### Дашборд преподавателя (`/v1/teacher`)

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/teacher/schedule` | `200` | Занятия за неделю (query: `week_start=YYYY-MM-DD`) |
| `GET` | `/v1/teacher/bot-requests` | `200` | Последние N запросов учеников боту (query: `limit=10`) |
| `GET` | `/v1/teacher/unconfirmed-lessons` | `200` | Занятия без `confirmed_by_student` за N дней (query: `days=2`) |
| `GET` | `/v1/teacher/pending-homework` | `200` | Занятия без `solution_received` за N дней (query: `days=2`) |
| `POST` | `/v1/teacher/remind-unconfirmed` | `200` | Отправить напоминание всем неподтвердившим |
| `POST` | `/v1/teacher/remind-pending-homework` | `200` | Отправить напоминание всем несдавшим ДЗ |
| `GET` | `/v1/teacher/reschedule-requests` | `200` | Активные запросы на перенос занятий |
| `PATCH` | `/v1/teacher/reschedule-requests/{id}` | `200` | Принять / отклонить запрос |

**Ключевые схемы ответов:**

`GET /v1/teacher/schedule` — список объектов занятий с флагами:
```json
{
  "items": [
    {
      "id": "uuid",
      "student_id": "uuid",
      "student_name": "string",
      "topic": "string",
      "scheduled_at": "ISO8601",
      "duration_minutes": 60,
      "status": "scheduled|completed|cancelled",
      "flags": {
        "notification_sent": false,
        "confirmed_by_student": false,
        "homework_sent": false,
        "solution_received": false,
        "solution_checked": false
      }
    }
  ],
  "total": 0
}
```

`GET /v1/teacher/bot-requests` — список сообщений из `messages` (role=user):
```json
{
  "items": [
    {
      "student_id": "uuid",
      "student_name": "string",
      "text": "string",
      "created_at": "ISO8601"
    }
  ]
}
```

`GET /v1/teacher/reschedule-requests`:
```json
{
  "items": [
    {
      "id": "bigint-as-string",
      "lesson_id": "uuid",
      "student_id": "uuid",
      "student_name": "string",
      "current_scheduled_at": "ISO8601",
      "proposed_time": "ISO8601",
      "requested_at": "ISO8601",
      "status": "pending"
    }
  ]
}
```

`PATCH /v1/teacher/reschedule-requests/{id}` — Request: `{ "status": "accepted"|"rejected" }`

---

### Ученики (`/v1/students`)

Заменяют и расширяют существующий `GET/POST /v1/users` — отдельный ресурс для удобства фронтенда.

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/students` | `200` | Список учеников с пагинацией (query: `limit`, `offset`) |
| `POST` | `/v1/students` | `201` | Создать ученика |
| `GET` | `/v1/students/{id}` | `200` | Профиль ученика |
| `PUT` | `/v1/students/{id}` | `200` | Обновить профиль |
| `DELETE` | `/v1/students/{id}` | `204` | Удалить ученика |
| `GET` | `/v1/students/{id}/lessons` | `200` | История занятий ученика (query: `limit`, `offset`) |
| `GET` | `/v1/students/{id}/dialogue` | `200` | Лента диалога ученика (query: `limit=20`, `offset=0`) |
| `GET` | `/v1/students/{id}/schedule` | `200` | Расписание на месяц (query: `month=YYYY-MM`) |

**Схема ученика (create/update request):**
```json
{
  "name": "string",
  "class_label": "string|null",
  "phone": "string|null",
  "email": "string|null",
  "telegram_id": "integer|null"
}
```

**Схема ответа `GET /v1/students`:**
```json
{
  "items": [{ "id": "uuid", "name": "string", "class_label": "...", "phone": "...", "email": "...", "telegram_id": 123, "created_at": "ISO8601" }],
  "total": 10,
  "limit": 50,
  "offset": 0
}
```

**Схема ответа `GET /v1/students/{id}/dialogue`:**
```json
{
  "items": [
    { "id": "uuid", "dialogue_id": "uuid", "role": "user|assistant", "content": "string", "created_at": "ISO8601" }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

**Схема ответа `GET /v1/students/{id}/schedule`:**
```json
{
  "month": "2026-04",
  "items": [
    {
      "id": "uuid",
      "topic": "string",
      "scheduled_at": "ISO8601",
      "duration_minutes": 60,
      "status": "scheduled|completed|cancelled",
      "notes": "string|null",
      "flags": { "confirmed_by_student": false, "homework_sent": false, "solution_received": false }
    }
  ]
}
```

---

### Занятия — расширение CRUD (`/v1/lessons`)

Существующие маршруты остаются; добавляются:

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `PUT` | `/v1/lessons/{id}` | `200` | Полное обновление занятия |
| `DELETE` | `/v1/lessons/{id}` | `204` | Удалить занятие |
| `PATCH` | `/v1/lessons/{id}/flags` | `200` | Обновить один или несколько флагов |

**Request `PUT /v1/lessons/{id}`:**
```json
{
  "student_id": "uuid",
  "topic": "string",
  "scheduled_at": "ISO8601",
  "duration_minutes": 60,
  "status": "scheduled|completed|cancelled",
  "notes": "string|null"
}
```

**Request `PATCH /v1/lessons/{id}/flags`:**
```json
{
  "notification_sent": true,
  "confirmed_by_student": null,
  "homework_sent": null,
  "solution_received": null,
  "solution_checked": null
}
```
(передаются только изменяемые флаги; `null` означает «не менять»)

---

### Настройки системы (`/v1/settings`)

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/settings` | `200` | Получить все настройки |
| `PUT` | `/v1/settings` | `200` | Обновить настройки |

**Схема:**
```json
{
  "teacher_name": "Владимир",
  "default_lesson_duration_minutes": 60,
  "lesson_reminder_hours_before": 24,
  "homework_reminder_hours_before": 48
}
```

---

## Что нужно сделать

1. Прочитать `docs/spec/frontend-requirements.md` — убедиться, что все экраны покрыты
2. Применить skill `api-design-principles`:
   - URL как ресурсы во мн.ч. (`/students`, `/lessons`)
   - HTTP-методы по семантике (`GET` — только чтение, `PUT` — полная замена, `PATCH` — частичное)
   - Единый формат ошибок: `{ "error": { "code": "...", "message": "..." } }`
   - `201` при создании, `204` при удалении без тела ответа
   - `PaginatedResponse` для list-endpoints
3. Дополнить `docs/tech/api-contracts.md`: добавить раздел «API для frontend» с описанием всех новых маршрутов
4. Проверить, что новый раздел не дублирует существующие MVP-маршруты

---

## Затрагиваемые файлы

| Действие | Файл |
|----------|------|
| Обновить (добавить раздел) | `docs/tech/api-contracts.md` |

---

## Критерии готовности

- [ ] Все новые маршруты описаны: метод, путь, query-параметры, request/response-схема, HTTP-коды ошибок
- [ ] Покрыты все 5 экранов: auth, teacher dashboard, students CRUD + detail, settings, student schedule
- [ ] CRUD занятий расширен: `PUT`, `DELETE`, `PATCH /flags`
- [ ] Нет дублирования с уже существующими MVP-контрактами
- [ ] Соблюдены принципы `api-design-principles`: ресурсы в мн.ч., правильные методы, единый формат ошибок
- [ ] `docs/tech/api-contracts.md` обновлён
