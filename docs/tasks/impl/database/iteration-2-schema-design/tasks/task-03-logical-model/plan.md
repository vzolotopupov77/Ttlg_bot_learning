# Задача 03: Актуализация логической модели — план

**Итерация:** 2 — Проектирование схемы данных  
**Задача:** 03 — Актуализация логической модели  
**Статус:** 📋 Planned

---

## Цель

Привести логическую модель в [`docs/data-model.md`](../../../../../../data-model.md) в соответствие с реализованными ORM-моделями (`storage/models.py`) и с требованиями, выявленными в итерации 1. Устранить все расхождения между документом и кодом.

## Источники

| Документ | Используемый раздел |
|----------|-------------------|
| [`backend/src/ttlg_backend/storage/models.py`](../../../../../../../../backend/src/ttlg_backend/storage/models.py) | Фактические типы, nullable, constraints |
| [`docs/tech/user-scenarios.md`](../../../../../../tech/user-scenarios.md) | Пробелы G-01…G-05, требующие решения |
| [`docs/data-model.md`](../../../../../../data-model.md) | Текущий документ — цель актуализации |

## Конкретные изменения

### 1. Первичные ключи

Во всех сущностях (`User`, `Lesson`, `Assignment`, `Progress`, `Dialogue`, `Message`) заменить `UUID / int` → `UUID`.

### 2. User

| Поле | Было | Станет |
|------|------|--------|
| `id` | `UUID / int` | `UUID` |
| `telegram_id` | `int (nullable)` | `BIGINT (nullable, unique)` |
| `created_at` | `datetime` | `TIMESTAMPTZ` |

### 3. Lesson

| Поле | Было | Станет |
|------|------|--------|
| `id` | `UUID / int` | `UUID` |
| `student_id` | `→ User` | `→ User (CASCADE)` |
| `teacher_id` | `→ User` | `→ User (CASCADE)` |
| `topic` | `string` | `VARCHAR(512)` |
| `scheduled_at` | `datetime` | `TIMESTAMPTZ` |

### 4. Assignment

| Поле | Было | Станет |
|------|------|--------|
| `id` | `UUID / int` | `UUID` |
| `lesson_id` | `→ Lesson (nullable)` | `→ Lesson (nullable, SET NULL)` |
| `student_id` | `→ User` | `→ User (CASCADE)` |

### 5. Progress

| Поле | Было | Станет |
|------|------|--------|
| `id` | `UUID / int` | `UUID` |
| `student_id` | `→ User` | `→ User (CASCADE)` |

### 6. Dialogue

| Поле | Было | Станет |
|------|------|--------|
| `id` | `UUID / int` | `UUID` |
| `student_id` | `→ User` | `→ User (CASCADE)` |
| `started_at` | `datetime` | `TIMESTAMPTZ` |

### 7. Message

| Поле | Было | Станет |
|------|------|--------|
| `id` | `UUID / int` | `UUID` |
| `dialogue_id` | `→ Dialogue` | `→ Dialogue (CASCADE)` |
| `created_at` | `datetime` | `TIMESTAMPTZ` |

### 8. Ширина строковых полей

Добавить в описание:
- `User.name` — `VARCHAR(255)`
- `Lesson.topic` — `VARCHAR(512)`

### 9. Пробелы схемы — решения

| ID | Пробел | Решение |
|----|--------|---------|
| G-01 | Нет `Topic` | Зафиксировать как «отложено до отдельной итерации»: в MVP `Lesson.topic` (VARCHAR(512)) достаточно; `Topic` как отдельная сущность — при появлении требований к базе материалов |
| G-02 | Нет `Material` | Отложено вместе с G-01; зависит от реализации SC-T-05 |
| G-03 | Нет механизма переноса занятия | Отложено: не блокирует MVP; при необходимости — флаг `reschedule_requested BOOLEAN` в `Lesson` |
| G-04 | `Progress` — пересчёт | Зафиксировать явно: пересчёт **вручную** (преподаватель обновляет через API); автоматический триггер — отложен |
| G-05 | `Lesson.notes` — одно поле | Подтверждено как достаточное для MVP |

## Затрагиваемые файлы

| Файл | Действие |
|------|---------|
| [`docs/data-model.md`](../../../../../../data-model.md) | Обновить таблицы всех сущностей; добавить примечание по пробелам G-01…G-05 |

## Definition of Done

- Каждое поле в документе соответствует колонке в ORM-модели: имя, тип (логический), nullable, cascade
- Enum-значения в документе совпадают с `StrEnum` в `models.py`
- PK всех сущностей задокументированы как `UUID`
- `telegram_id` помечен как `BIGINT, unique`
- Timestamps — `TIMESTAMPTZ`
- Решения по пробелам G-01…G-05 зафиксированы явно (принято / отложено / отклонено с обоснованием)
- Расхождения с предыдущей версией задокументированы в summary задачи
