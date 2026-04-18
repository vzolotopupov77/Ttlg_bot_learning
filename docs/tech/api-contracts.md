# HTTP API: контракты (backend)

Человекочитаемое описание публичных маршрутов. **Актуальные схемы полей** — в OpenAPI на `GET /docs` у запущенного backend и в [integrations.md](../integrations.md) (сводка + smoke). Общие правила (префикс `/v1`, ошибки, коды) — [api-conventions.md](../api-conventions.md). Сущности БД — [data-model.md](../data-model.md).

---

## Обзор маршрутов (MVP)

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `POST` | `/v1/users` | `201` | Создать пользователя |
| `GET` | `/v1/users/{user_id}` | `200` | Получить пользователя |
| `GET` | `/v1/users/{user_id}/progress` | `200` | Сводка прогресса ученика (агрегаты по занятиям и ДЗ) |
| `POST` | `/v1/lessons` | `201` | Создать занятие |
| `GET` | `/v1/lessons/{lesson_id}` | `200` | Получить занятие |
| `PATCH` | `/v1/lessons/{lesson_id}/status` | `200` | Обновить статус занятия |
| `POST` | `/v1/assignments` | `201` | Создать домашнее задание |
| `GET` | `/v1/assignments/{assignment_id}` | `200` | Получить ДЗ |
| `PATCH` | `/v1/assignments/{assignment_id}/status` | `200` | Обновить статус ДЗ |
| `POST` | `/v1/dialogue/message` | `200` | Сообщение в диалог; ответ ассистента |

Проверка готовности (без префикса версии): `GET /health` → `200` при доступной БД, иначе `503` (см. реализацию).

Детальные тела запросов/ответов и enum-значения — в **OpenAPI**; ниже — расширенное описание сценария диалога и типовых ошибок.

Типичный `404` для CRUD по сущности: `error.code` = `not_found`. Для диалога — отдельные коды (см. ниже).

**Профиль и занятия:** в схемах `User` (создание/чтение) доступны опциональные `class_label`, `phone`, `email`; у `Lesson` — `duration_minutes` (по умолчанию 60). См. [data-model.md](../data-model.md) и OpenAPI.

---

## `POST /v1/dialogue/message`

Сценарий: ученик задаёт вопрос ассистенту; backend сохраняет историю в `Dialogue` / `Message`, подмешивает контекст занятий и ДЗ в промпт, вызывает LLM и возвращает ответ.

### Предусловие

Учёнок с данным `telegram_id` **должен уже существовать** в БД (обычно `POST /v1/users` с `role`: `student` и тем же `telegram_id`). Иначе — `404` `user_not_found`.

### Назначение

| | |
|---|---|
| **Метод / путь** | `POST /v1/dialogue/message` |
| **Клиенты** | Telegram-бот (основной путь сейчас); веб — тот же контракт по `telegram_id`, пока нет отдельной модели сессии |

### Заголовки запроса

| Заголовок | Значение | Обязательно |
|-----------|----------|-------------|
| `Content-Type` | `application/json` | да |
| `X-User-Role` | `student` | нет (MVP placeholder; эндпоинт заголовок не интерпретирует) |

### Request (JSON)

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| `telegram_id` | `integer` | да | Поиск `User` с `role=student` |
| `text` | `string` | да | Текст вопроса; не пустая строка после trim |
| `dialogue_id` | `string` (UUID) | нет | Продолжить существующий `Dialogue`; если нет — создать новый |

Пример:

```json
{
  "telegram_id": 123456789,
  "text": "Как решить квадратное уравнение?",
  "dialogue_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response `200 OK` (JSON)

| Поле | Тип | Описание |
|------|-----|----------|
| `dialogue_id` | `string` (UUID) | `Dialogue.id` |
| `message_id` | `string` (UUID) | `Message.id` ответа ассистента (`role=assistant`) |
| `text` | `string` | Текст ответа ассистента |
| `created_at` | `string` (ISO 8601, UTC) | Время создания сообщения ассистента; в ответе без дробной части секунды, суффикс `Z` |

Пользовательское сообщение (`role=user`) также сохраняется; его `id` в этом контракте не возвращается (при необходимости расширить позже).

Пример:

```json
{
  "dialogue_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "text": "Квадратное уравнение — это …",
  "created_at": "2026-03-29T10:00:00Z"
}
```

### Соответствие модели данных

- `Dialogue`: `student_id` ← `User` по `telegram_id`; поле `channel` в модели допускает `telegram` и `web`, но **текущая реализация этого эндпоинта при создании диалога всегда выставляет `telegram`**. Поддержка явного выбора канала (для веб-клиента) — отдельное расширение API.
- `Message`: `dialogue_id`, `role` (`user` | `assistant`), `content`, `created_at`.

### Ошибки

Формат тела — [api-conventions.md](../api-conventions.md). Типовые случаи:

| HTTP | `error.code` (ориентир) | Причина |
|------|-------------------------|---------|
| `422` | `validation_error` | Невалидное тело, пустой `text` и т.п. |
| `404` | `user_not_found` | Нет пользователя с таким `telegram_id` или роль не `student` |
| `404` | `dialogue_not_found` | Неизвестный `dialogue_id` **или** диалог принадлежит другому пользователю (намеренно не различать, чтобы не раскрывать чужие id) |
| `503` | `llm_unavailable` | Таймаут / ошибка провайдера LLM |
| `500` | `internal_error` | Внутренняя ошибка без утечки деталей |

---

## API для frontend (проект)

Ниже — контракты для веб-клиента (см. [frontend-requirements.md](../spec/frontend-requirements.md)). Реализация — итерация backend по [tasklist-frontend.md](../tasks/tasklist-frontend.md). Существующие маршруты MVP (таблица в начале документа) **не дублируются**; при коллизии имён приоритет у этого раздела после внедрения.

**Аутентификация:** после успешного `POST /v1/auth/login` сессия передаётся через **httpOnly cookie** с JWT (имя cookie и атрибуты — в реализации; `Secure`/`SameSite` — по среде). Заголовок `Authorization: Bearer` допускается как альтернатива для Swagger — целевой путь для браузера — cookie.

**Ошибки:** формат [api-conventions.md](../api-conventions.md) — `{"error": {"code": "...", "message": "..."}}`.

**Пагинация списков:** ответы вида `{ "items": [...], "total": number, "limit": number, "offset": number }`, если не указано иное.

---

### Аутентификация

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `POST` | `/v1/auth/login` | `200` | Вход: e-mail, пароль, роль |
| `POST` | `/v1/auth/logout` | `204` | Выход (очистка cookie) |
| `GET` | `/v1/auth/me` | `200` | Текущий пользователь |

**`POST /v1/auth/login`** — body:

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| `email` | `string` | да | **Логин — e-mail** пользователя; формат и уникальность — в реализации (сопоставление с `users.email`) |
| `password` | `string` | да | Пароль |
| `role` | `string` | да | `teacher` \| `student` — должна совпадать с ролью пользователя в БД |

Response `200`: `{ "user": { "id": "uuid", "name": "string", "role": "teacher"|"student" } }` — без токена в JSON при модели cookie-only; если возвращается одноразовый токен — только до установки cookie (уточняется в реализации).

Ошибки: `401` `invalid_credentials`; `422` `validation_error`.

**`GET /v1/auth/me`** — Response `200`: `{ "id": "uuid", "name": "string", "role": "teacher"|"student" }`. Ошибка: `401` `unauthorized`.

---

### Преподаватель (`/v1/teacher`)

Все маршруты — только для `role=teacher`, иначе `403` `forbidden`.

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/teacher/schedule` | `200` | Недельное расписание |
| `GET` | `/v1/teacher/bot-requests` | `200` | Последние сообщения учеников боту |
| `GET` | `/v1/teacher/unconfirmed-lessons` | `200` | Неподтверждённые занятия за окно дней |
| `GET` | `/v1/teacher/pending-homework` | `200` | Занятия с несданным ДЗ за окно дней |
| `POST` | `/v1/teacher/remind-unconfirmed` | `200` | Напоминание неподтвердившим |
| `POST` | `/v1/teacher/remind-pending-homework` | `200` | Напоминание по несданным ДЗ |
| `GET` | `/v1/teacher/reschedule-requests` | `200` | Запросы на перенос |
| `PATCH` | `/v1/teacher/reschedule-requests/{request_id}` | `200` | Принять / отклонить запрос |

Query-параметры:

- `GET .../schedule` — `week_start` (date `YYYY-MM-DD`, понедельник недели).
- `GET .../bot-requests` — `limit` (default `10`, max по реализации).
- `GET .../unconfirmed-lessons`, `GET .../pending-homework` — `days` (default `2`).

**Пример элемента занятия в расписании** (поля могут называться иначе в OpenAPI, смысл сохраняется):

```json
{
  "id": "uuid",
  "student_id": "uuid",
  "student_name": "string",
  "topic": "string",
  "scheduled_at": "2026-04-06T07:00:00Z",
  "ends_at": "2026-04-06T08:00:00Z",
  "duration_minutes": 60,
  "status": "scheduled",
  "flags": {
    "notification_sent": false,
    "confirmed_by_student": false,
    "homework_sent": false,
    "solution_received": false,
    "solution_checked": false
  }
}
```

**`PATCH /v1/teacher/reschedule-requests/{request_id}`** — body: `{ "status": "accepted" | "rejected" }`.

---

### Ученики (преподаватель) — `/v1/students`

Только `role=teacher`, иначе `403`.

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/students` | `200` | Список учеников |
| `POST` | `/v1/students` | `201` | Создать ученика (`role=student`) |
| `GET` | `/v1/students/{id}` | `200` | Профиль |
| `PUT` | `/v1/students/{id}` | `200` | Обновить профиль |
| `DELETE` | `/v1/students/{id}` | `204` | Удалить |
| `GET` | `/v1/students/{id}/lessons` | `200` | История занятий |
| `GET` | `/v1/students/{id}/dialogue` | `200` | Сообщения диалога (бот / ассистент) |
| `GET` | `/v1/students/{id}/stats` | `200` | Агрегаты для карточек на детальной странице (опционально; может быть частью `GET .../{id}`) |

**`POST` body** (создание ученика):

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `string` | ФИО |
| `class_label` | `string` \| `null` | Класс |
| `phone` | `string` \| `null` | Телефон |
| `email` | `string` \| `null` | Email |
| `notes` | `string` \| `null` | Заметки / цель обучения |
| `telegram_id` | `integer` \| *отсутствует* \| `null` | Необязательно; целое **≥ 1**; соответствует `users.telegram_id` (уникально в БД) |

**`PUT` body** (обновление ученика): те же поля, что и в `POST`, плюс обязательное поле **`telegram_id`** в JSON (значение `integer` или `null` для сброса привязки). Остальные поля с профилем по-прежнему опциональны с точки зрения семантики формы, но клиенту рекомендуется передавать полный набор, как в веб-форме.

**Ответ `StudentRead` / элементы списка:** те же поля, включая `telegram_id`: `integer` \| `null`.

Конфликт уникальности: при занятом `telegram_id` у другого пользователя — **`409`** `conflict` (текст вроде «Telegram ID already in use»), аналогично занятому e-mail.

**`GET .../{id}/lessons`** — каждый элемент содержит `flags`: `notification_sent`, `confirmed_by_student`, `homework_sent`, `solution_received`, `solution_checked` (как в недельном расписании).

**`GET .../{id}/stats`** — агрегаты прогресса; дополнительно `lessons_solution_checked` — число занятий ученика с проверенным решением (`solution_checked`).

**`GET .../dialogue`** — query: `limit`, `offset` (сортировка: от старых к новым или наоборот — зафиксировать в OpenAPI; для UI «скролл вверх» удобен порядок от новых к старым с подгрузкой старых).

---

### Занятия — расширение CRUD

Базовые маршруты MVP — в таблице в начале файла. Дополнительно:

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `PUT` | `/v1/lessons/{lesson_id}` | `200` | Полная замена полей занятия |
| `DELETE` | `/v1/lessons/{lesson_id}` | `204` | Удалить |
| `PATCH` | `/v1/lessons/{lesson_id}/flags` | `200` | Обновить флаги (частично; вызывается при каждом переключении в UI) |

**`PATCH .../flags`** — body: только изменяемые поля из набора `notification_sent`, `confirmed_by_student`, `homework_sent`, `solution_received`, `solution_checked` (`boolean`).

**`PUT /v1/lessons/{id}`** — поля согласуются с моделью `Lesson` + `student_id`, `scheduled_at`, `ends_at` или `duration_minutes` (один из вариантов — в OpenAPI).

---

### Настройки системы

Только `role=teacher`.

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/settings` | `200` | Текущие настройки |
| `PUT` | `/v1/settings` | `200` | Сохранить |

**Body / Response** (пример):

```json
{
  "teacher_name": "string",
  "default_lesson_duration_minutes": 60,
  "lesson_reminder_hours_before": 24,
  "homework_reminder_hours_before": 48
}
```

Хранение — например таблица key-value (`system_settings`); детали — в миграциях.

---

### Расписание ученика (свой контекст)

Только `role=student`; отдаётся расписание **текущего** пользователя.

| Метод | Путь | Успех | Назначение |
|-------|------|-------|------------|
| `GET` | `/v1/student/schedule` | `200` | Недельное расписание ученика |

Query: `week_start` (`YYYY-MM-DD`). Структура ответа — как у `/v1/teacher/schedule`, но без чужих учеников и без преподавательских панелей на UI.

Альтернатива: `GET /v1/students/{id}/schedule` с проверкой `id == auth.user.id` — допустимо, если унифицировать клиент; целевой упрощённый путь — `/v1/student/schedule`.

---

### Проверка по api-design-principles

Ниже — сверка раздела «API для frontend» с принципами REST-ориентированного API (ресурсы, методы, коды, единообразие). Использован skill **api-design-principles**.

| Принцип | Оценка | Комментарий |
|--------|--------|-------------|
| Ресурсы в URL — существительные, множественное число для коллекций | ✅ | `/v1/students`, `/v1/lessons`, вложенные `/lessons/{id}/flags`. |
| Семантика HTTP | ✅ | `GET` — чтение, `POST` — создание/действия, `PUT` — полная замена, `PATCH` — частично, `DELETE` — удаление; `201`/`204` где уместно. |
| Синглтон-настройки | ✅ | `GET`/`PUT /v1/settings` — уместное именование для одного набора настроек. |
| Контекст «текущий пользователь» | ✅ | `GET /v1/student/schedule` без `id` в пути — допустимый паттерн для «me»-ресурса. |
| Пагинация | ✅ | `items` + `total` + `limit` + `offset`; явно указаны query для `GET /v1/students` — см. ниже. |
| Ошибки | ✅ | Единый объект `error` ([api-conventions.md](../api-conventions.md)); коды `snake_case`. |
| Команды (не CRUD) | ⚠️ осознанно | `POST .../remind-unconfirmed`, `.../remind-pending-homework` — **action-style** (RPC). Для доменных команд допустимо; при эволюции API возможны варианты вроде `POST /v1/teacher/unconfirmed-lessons:remind` или подресурс `.../reminders`. |
| Идемпотентность напоминаний | ⚠️ | Повторный `POST` может продублировать рассылку; при необходимости — `Idempotency-Key` (отдельная задача). |

**Дополнения к контракту (после ревью):**

- `GET /v1/students` — query: `limit` (default `50`, max по реализации), `offset` (default `0`).
- `POST /v1/teacher/remind-unconfirmed`, `POST /v1/teacher/remind-pending-homework` — response `200` с телом, например `{ "notified_count": number }` (точное имя — в OpenAPI).
- `POST /v1/students` — при конфликте уникальности (e-mail или **telegram_id** уже заняты) — `409` `conflict` (или узкоспециализированный `code`).
- `PATCH /v1/teacher/reschedule-requests/{request_id}` — при уже обработанном запросе — `409` `conflict` или `422` `validation_error` (зафиксировать в OpenAPI).
- `GET /v1/teacher/schedule` — response: обёртка с полем `items` (массив занятий недели) и при необходимости `week_start` для проверки на клиенте.

---

## Заметки по дизайну

**URL-иерархия.** Текущий путь `POST /v1/dialogue/message` — action-style (нет явного `{dialogue_id}` в URL). Это достаточно для MVP. При эволюции API возможный вариант: `POST /v1/dialogues` (создать диалог) + `POST /v1/dialogues/{dialogue_id}/messages` (добавить сообщение). Менять сейчас не нужно; учесть при проектировании следующих версий.

**Идемпотентность.** Повторный запрос при обрыве сети создаст дубль сообщения и вызов LLM. Если потребуется защита — добавить заголовок `Idempotency-Key` (отдельная задача).

**Rate limiting.** Вне текущего контракта; актуально при выходе в продакшн.

**Дублирование OpenAPI.** Новые публичные эндпоинты добавлять в код и в Swagger; в этом файле — краткая цель маршрута и нестандартная семантика (как у диалога). Полные Pydantic-схемы дублировать сюда не обязательно.
