# Задача 05 — Миграция с mock-данными: план

## Цель

Создать Alembic-миграцию с seed-данными, достаточными для демонстрации всех 5 экранов frontend без ручного ввода. После `alembic upgrade head` БД содержит учеников, занятия с флагами, домашние задания, диалоги, запросы на перенос и настройки системы.

## Предусловие

Задача 04 завершена: DDL-миграции применены, таблицы `reschedule_requests`, `system_settings`, флаги в `lessons`, `password_hash` в `users` — существуют.

## Принципы создания seed-миграции

- **Отдельный файл** — не смешивать DDL и DML в одной миграции
- `downgrade()` — удаляет только seed-записи (не таблицы)
- UUID генерировать через `gen_random_uuid()` (PostgreSQL) или хардкод фиксированных UUID для воспроизводимости
- Временны́е метки — относительно момента применения (`now()`) или абсолютные фиксированные даты для стабильности тестов

## Состав seed-данных

### Ученики (4–6 записей, `role=student`)

| name | class_label | phone | email | telegram_id | notes |
|------|-------------|-------|-------|-------------|-------|
| Алексей Иванов | 10А | +7 900 100-01-01 | alex@example.com | 100000001 | Готовится к ЕГЭ по математике |
| Мария Петрова | 9Б | +7 900 100-01-02 | maria@example.com | 100000002 | Нужна помощь с алгеброй |
| Дмитрий Сидоров | 11А | +7 900 100-01-03 | dmitry@example.com | 100000003 | Целевое поступление в МФТИ |
| Анна Козлова | 8В | +7 900 100-01-04 | anna@example.com | 100000004 | Базовый уровень |
| Иван Новиков | 10Б | +7 900 100-01-05 | ivan@example.com | 100000005 | null |

`password_hash` — `NULL` для учеников (вход только через Telegram).

### Занятия (20–30 записей)

Охват: за последние 4 недели и ближайшие 2 недели.

**Разнообразие статусов и флагов:**

| Период | Статус | Флаги (примеры) |
|--------|--------|----------------|
| -4 нед. | `completed` | все флаги `true` |
| -3 нед. | `completed` | `homework_sent=true`, `solution_received=false`, `solution_checked=false` |
| -2 нед. | `completed` | `confirmed_by_student=true`, `homework_sent=true`, `solution_received=true` |
| -1 нед. | `completed` | смешанные флаги |
| текущая | `scheduled` | `notification_sent=true`, `confirmed_by_student=false` (→ неподтверждённые) |
| +1 нед. | `scheduled` | `notification_sent=false` (будущие, без уведомлений) |

Минимум 2–3 занятия с `confirmed_by_student=false` в ближайшие 2 дня (для блока неподтверждённых).
Минимум 2–3 занятия с `homework_sent=true`, `solution_received=false` за последние 2 дня (для блока несданных ДЗ).

### Домашние задания (10–15 записей)

| assignment | status |
|-----------|--------|
| «Задачи на квадратные уравнения, §5 упр. 1–10» | `submitted` |
| «Контрольная работа по тригонометрии» | `overdue` |
| «Функции и графики, §8» | `pending` |
| «Производные, §12 упр. 3–7» | `pending` |
| ... | ... |

Минимум: 3 `pending`, 3 `submitted`, 3 `overdue` — по разным ученикам.

### Диалоги и сообщения (2–3 диалога)

- По 8–12 сообщений в каждом диалоге
- Чередование `role=user` и `role=assistant`
- Содержание — вопросы по математике и ответы ассистента (реалистичные примеры)
- `channel=telegram`

Пример диалога:
```
user: "Как решить уравнение x² - 5x + 6 = 0?"
assistant: "Это квадратное уравнение. Используем формулу дискриминанта: D = b² - 4ac = 25 - 24 = 1..."
user: "А что если дискриминант отрицательный?"
assistant: "Если D < 0, уравнение не имеет действительных корней..."
```

### Запросы на перенос (2–3 записи)

| lesson | student | proposed_time | status |
|--------|---------|--------------|--------|
| ближайшее занятие ученика 1 | ученик 1 | +2 дня от занятия | `pending` |
| занятие -3 дня ученика 2 | ученик 2 | +1 неделя | `pending` |
| занятие -5 дней ученика 3 | ученик 3 | уже обработан | `accepted` |

### Настройки системы

```sql
INSERT INTO system_settings (key, value) VALUES
  ('teacher_name', 'Владимир'),
  ('default_lesson_duration_minutes', '60'),
  ('lesson_reminder_hours_before', '24'),
  ('homework_reminder_hours_before', '48');
```

## Имя файла миграции

```
backend/alembic/versions/2026_04_12_008_seed_mock_data.py
```

> Номер уточняется по последней применённой миграции.

## Структура миграции

```python
"""Seed mock data for frontend development."""

revision = "..."
down_revision = "..."  # последняя DDL-миграция из задачи 04

def upgrade() -> None:
    op.execute("""
        INSERT INTO users ...
        INSERT INTO lessons ...
        INSERT INTO assignments ...
        INSERT INTO dialogues ...
        INSERT INTO messages ...
        INSERT INTO reschedule_requests ...
        INSERT INTO system_settings ...
    """)

def downgrade() -> None:
    op.execute("""
        DELETE FROM system_settings WHERE key IN (...);
        DELETE FROM reschedule_requests WHERE ...;
        DELETE FROM messages WHERE ...;
        DELETE FROM dialogues WHERE ...;
        DELETE FROM assignments WHERE ...;
        DELETE FROM lessons WHERE ...;
        DELETE FROM users WHERE email LIKE '%@example.com';
    """)
```

> Использовать фиксированные UUID для seed-записей — чтобы `downgrade` был детерминированным.

## Проверка

После `alembic upgrade head`:

```bash
# Через Swagger / httpx:
GET /v1/students           → ≥ 4 записи
GET /v1/teacher/schedule   → непустые данные (занятия текущей недели)
GET /v1/teacher/bot-requests → ≥ 5 сообщений
GET /v1/teacher/unconfirmed-lessons → ≥ 2 записи
GET /v1/teacher/pending-homework    → ≥ 2 записи
GET /v1/teacher/reschedule-requests → ≥ 2 записи
GET /v1/settings           → все 4 ключа
```

## Артефакты

- `backend/alembic/versions/2026_04_12_008_seed_mock_data.py`
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-05-mock-migration/plan.md` (этот файл)
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-05-mock-migration/summary.md` — после выполнения

## Definition of Done

**Агент:**

- [ ] Миграция применяется без ошибок: `alembic upgrade head`
- [ ] `alembic downgrade -1` + `alembic upgrade head` — цикл работает без ошибок
- [ ] `GET /v1/teacher/schedule` → непустые данные
- [ ] `GET /v1/students` → ≥ 4 учеников
- [ ] `GET /v1/teacher/bot-requests` → ≥ 5 записей
- [ ] `GET /v1/teacher/unconfirmed-lessons` → ≥ 2 записи
- [ ] `GET /v1/teacher/reschedule-requests` → ≥ 2 записи
- [ ] `GET /v1/settings` → 4 ключа

**Пользователь:**

- [ ] `make backend-migrate` — миграция прошла
- [ ] `GET /v1/students` в Swagger — виден список учеников
