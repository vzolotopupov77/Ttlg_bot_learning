# Задача 03 — Анализ пробелов схемы данных: план

## Цель

Выявить все расхождения между текущей схемой `docs/data-model.md` и требованиями 5 экранов (Итерация 0); обновить `docs/data-model.md` с учётом новых таблиц, полей, FK и индексов; сформулировать необходимые Alembic-миграции.

## Входные данные

| Файл | Роль |
|------|------|
| [docs/data-model.md](../../../../../data-model.md) | Текущая схема |
| [docs/tech/api-contracts.md](../../../../../tech/api-contracts.md) | API-контракты frontend |
| [docs/spec/frontend-requirements.md](../../../../../spec/frontend-requirements.md) | Требования к экранам |
| [backend/src/ttlg_backend/storage/models.py](../../../../../../backend/src/ttlg_backend/storage/models.py) | ORM-модели |

## Анализ расхождений

### Таблица `users`

| Поле | Текущее состояние | Требование | Действие |
|------|------------------|------------|---------|
| `password_hash` | Отсутствует | `TEXT NULL` (auth) | Добавить |
| `notes` | Отсутствует | `TEXT NULL` (профиль ученика) | Добавить |

**Решение по `password_hash`:** добавить как `TEXT NULL` (nullable до полной миграции данных). Добавление `NOT NULL` требует двухшаговой миграции — отложить до Задачи 06 (когда вставляется реальный хеш).

### Таблица `lessons`

| Поле | Текущее состояние | Требование | Действие |
|------|------------------|------------|---------|
| `notification_sent` | Отсутствует | `BOOLEAN NOT NULL DEFAULT false` | Добавить |
| `confirmed_by_student` | Отсутствует | `BOOLEAN NOT NULL DEFAULT false` | Добавить |
| `homework_sent` | Отсутствует | `BOOLEAN NOT NULL DEFAULT false` | Добавить |
| `solution_received` | Отсутствует | `BOOLEAN NOT NULL DEFAULT false` | Добавить |
| `solution_checked` | Отсутствует | `BOOLEAN NOT NULL DEFAULT false` | Добавить |

**Решение:** 5 флагов добавить одной миграцией с `DEFAULT false`; добавление `NOT NULL` с `DEFAULT` (non-volatile) — безопасно для PostgreSQL, не вызывает полного rewrite таблицы.

### Новая таблица `reschedule_requests`

```sql
reschedule_requests
  id             BIGINT GENERATED ALWAYS AS IDENTITY  PRIMARY KEY
  lesson_id      BIGINT NOT NULL  REFERENCES lessons(id) ON DELETE CASCADE
  student_id     BIGINT NOT NULL  REFERENCES users(id) ON DELETE CASCADE
  proposed_time  TIMESTAMPTZ NOT NULL
  requested_at   TIMESTAMPTZ NOT NULL  DEFAULT now()
  status         TEXT NOT NULL  DEFAULT 'pending'
                 CHECK (status IN ('pending', 'accepted', 'rejected'))

CREATE INDEX ON reschedule_requests (lesson_id);
CREATE INDEX ON reschedule_requests (student_id);
```

> **Примечание:** В текущей схеме PK у `lessons` и `users` — UUID, а не BIGINT. Следовательно, FK-колонки в `reschedule_requests` также должны быть UUID:
> `lesson_id UUID NOT NULL REFERENCES lessons(id)`,
> `student_id UUID NOT NULL REFERENCES users(id)`.
> PK таблицы `reschedule_requests`: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` (для согласованности со схемой проекта).

### Новая таблица `system_settings`

```sql
system_settings
  key    TEXT  PRIMARY KEY
  value  TEXT  NOT NULL
```

Хранит именованные настройки, например:
- `teacher_name`
- `default_lesson_duration_minutes`
- `lesson_reminder_hours_before`
- `homework_reminder_hours_before`

## Необходимые миграции Alembic

| № | Название | Содержание |
|---|---------|-----------|
| 1 | `2026_04_12_004_add_lesson_flags.py` | 5 bool-колонок в `lessons` |
| 2 | `2026_04_12_005_add_user_auth_fields.py` | `password_hash`, `notes` в `users` |
| 3 | `2026_04_12_006_add_reschedule_requests.py` | Новая таблица + индексы |
| 4 | `2026_04_12_007_add_system_settings.py` | Новая таблица |

> Имена уточняются при создании; пронумеровать последовательно после последней существующей миграции `5dcbe7dd0861`.

## Изменения в `docs/data-model.md`

1. Добавить поля `password_hash`, `notes` в раздел `User`
2. Добавить 5 флагов в раздел `Lesson`
3. Добавить разделы `RescheduleRequest` и `SystemSettings`
4. Обновить ER-диаграмму (новые сущности и связи)
5. Обновить физическую схему (типы, constraints, индексы)
6. Обновить таблицу FK-каскадов и индексов
7. Закрыть пробел G-03 в разделе «Пробелы схемы»

## Изменения в ORM-моделях

Файл: `backend/src/ttlg_backend/storage/models.py`

- `User`: добавить `password_hash: Mapped[str | None]`, `notes: Mapped[str | None]`
- `Lesson`: добавить 5 `Mapped[bool]` с `server_default="false"`
- Новый класс `RescheduleRequest(Base)` с полями, FK, индексами
- Новый класс `SystemSetting(Base)` с `key` как PK

## Правила (postgresql-table-design)

- `BOOLEAN NOT NULL DEFAULT false` — не nullable, не int
- `TEXT` вместо `VARCHAR(n)` для `key` и `value` в `system_settings`
- `TIMESTAMPTZ` для всех временных полей
- FK-колонки в `reschedule_requests` — обязательные явные индексы (PostgreSQL не индексирует FK автоматически)
- `CHECK (status IN ('pending', 'accepted', 'rejected'))` — не enum-тип (проще для миграций)

## Артефакты

- `docs/data-model.md` — обновлён
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/plan.md` (этот файл)
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/summary.md` — после выполнения

## Definition of Done

**Агент:**

- [ ] Все пробелы перечислены в summary с обоснованием
- [ ] `docs/data-model.md` обновлён: новые таблицы, поля, FK, индексы, ER-диаграмма
- [ ] Нет `VARCHAR(n)`, `TIMESTAMP` (без TZ), nullable bool-флагов в новых таблицах
- [ ] FK-колонки в `reschedule_requests` имеют явные индексы
- [ ] Нет противоречий с уже принятыми ADR
- [ ] ORM-модели (`models.py`) синхронизированы с документом

**Пользователь:**

- [ ] Открыть `docs/data-model.md` — убедиться в наличии `reschedule_requests`, `system_settings`, флагов в `lessons`, `password_hash` в `users`
