# Задача 04: Физическая ER-диаграмма — план

**Итерация:** 2 — Проектирование схемы данных  
**Задача:** 04 — Физическая ER-диаграмма  
**Статус:** 📋 Planned

---

## Цель

Добавить в [`docs/data-model.md`](../../../../../../data-model.md) новую секцию «Физическая схема»: Mermaid-диаграмму с PostgreSQL-типами, nullable, constraints; таблицу FK-каскадов; таблицу индексов. Диаграмма должна давать достаточно информации для ревью и работы с `psql`.

## Источники

| Документ | Используемый раздел |
|----------|-------------------|
| [`backend/src/ttlg_backend/storage/models.py`](../../../../../../../../backend/src/ttlg_backend/storage/models.py) | Фактические типы, nullable, ForeignKey, cascade, index |
| [`docs/data-model.md`](../../../../../../data-model.md) | Актуализированная логическая модель (задача 03) |

## Состав секции «Физическая схема»

### Mermaid erDiagram — маппинг типов

| ORM (SQLAlchemy) | PostgreSQL-тип |
|------------------|----------------|
| `Uuid(as_uuid=True)` | `UUID` |
| `String(255)` | `VARCHAR(255)` |
| `String(512)` | `VARCHAR(512)` |
| `Text` | `TEXT` |
| `BigInteger()` | `BIGINT` |
| `Date` | `DATE` |
| `DateTime(timezone=True)` | `TIMESTAMPTZ` |
| `Integer` (int mapped_column) | `INT` |
| `SQLEnum(... native_enum=True)` | PostgreSQL enum-тип |

### Сущности и их PostgreSQL-поля

**users**
```
id            UUID         NOT NULL  PK
role          user_role    NOT NULL
name          VARCHAR(255) NOT NULL
telegram_id   BIGINT       NULL      UNIQUE
created_at    TIMESTAMPTZ  NOT NULL  DEFAULT now()
```

**lessons**
```
id            UUID         NOT NULL  PK
student_id    UUID         NOT NULL  FK → users.id
teacher_id    UUID         NOT NULL  FK → users.id
topic         VARCHAR(512) NOT NULL
scheduled_at  TIMESTAMPTZ  NOT NULL
status        lesson_status NOT NULL
notes         TEXT         NULL
```

**assignments**
```
id            UUID              NOT NULL  PK
lesson_id     UUID              NULL      FK → lessons.id
student_id    UUID              NOT NULL  FK → users.id
description   TEXT              NOT NULL
due_date      DATE              NOT NULL
status        assignment_status NOT NULL
```

**progress**
```
id                UUID  NOT NULL  PK
student_id        UUID  NOT NULL  FK → users.id
period_start      DATE  NOT NULL
period_end        DATE  NOT NULL
lessons_completed INT   NOT NULL  DEFAULT 0
assignments_done  INT   NOT NULL  DEFAULT 0
assignments_total INT   NOT NULL  DEFAULT 0
summary           TEXT  NULL
```

**dialogues**
```
id            UUID             NOT NULL  PK
student_id    UUID             NOT NULL  FK → users.id
channel       dialogue_channel NOT NULL
started_at    TIMESTAMPTZ      NOT NULL  DEFAULT now()
```

**messages**
```
id            UUID         NOT NULL  PK
dialogue_id   UUID         NOT NULL  FK → dialogues.id
role          message_role NOT NULL
content       TEXT         NOT NULL
created_at    TIMESTAMPTZ  NOT NULL  DEFAULT now()
```

### Таблица FK-каскадов

| FK | ON DELETE |
|----|-----------|
| `lessons.student_id` → `users.id` | CASCADE |
| `lessons.teacher_id` → `users.id` | CASCADE |
| `assignments.student_id` → `users.id` | CASCADE |
| `assignments.lesson_id` → `lessons.id` | SET NULL |
| `progress.student_id` → `users.id` | CASCADE |
| `dialogues.student_id` → `users.id` | CASCADE |
| `messages.dialogue_id` → `dialogues.id` | CASCADE |

### Таблица индексов

| Таблица | Колонка(и) | Тип | Источник |
|---------|-----------|-----|---------|
| `users` | `telegram_id` | UNIQUE INDEX | `unique=True` в ORM |
| `lessons` | `student_id` | INDEX | `index=True` в ORM |
| `lessons` | `teacher_id` | INDEX | `index=True` в ORM |
| `assignments` | `student_id` | INDEX | `index=True` в ORM |
| `assignments` | `lesson_id` | INDEX | `index=True` в ORM |
| `progress` | `student_id` | INDEX | `index=True` в ORM |
| `dialogues` | `student_id` | INDEX | `index=True` в ORM |
| `messages` | `dialogue_id` | INDEX | `index=True` в ORM |

> Дополнительные составные индексы (например `(dialogue_id, created_at)` на `messages`) рассматриваются в задаче 05.

## Затрагиваемые файлы

| Файл | Действие |
|------|---------|
| [`docs/data-model.md`](../../../../../../data-model.md) | Добавить секцию «Физическая схема» после существующей логической ERD |

## Definition of Done

- ERD содержит все 6 сущностей: `users`, `lessons`, `assignments`, `progress`, `dialogues`, `messages`
- Для каждой колонки указан PostgreSQL-тип и nullable
- FK каскады (`CASCADE`, `SET NULL`) указаны явно и соответствуют `models.py`
- Ключевые индексы перечислены (минимум: все `index=True` из ORM + `telegram_id UNIQUE`)
- Секция добавлена отдельно от логической ERD и не заменяет её
