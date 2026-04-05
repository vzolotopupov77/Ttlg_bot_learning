# Задача 11: Актуализация ORM-моделей — итог

**Дата:** 2026-04-05  
**Статус:** ✅ Done

## Что сделано

Применены все отложенные пункты из summary задачи 05:

| Пункт | Результат |
|-------|-----------|
| R-03 | `UniqueConstraint("uq_progress_student_period")` добавлен в `Progress.__table_args__` |
| R-04 | `Index("ix_messages_dialogue_created", "dialogue_id", "created_at")` добавлен в `Message.__table_args__` |
| R-05 | `Index("ix_lessons_scheduled_at", "scheduled_at")` добавлен в `Lesson.__table_args__` |
| R-07 | `updated_at` на `Lesson`/`Assignment` — **отложено**: нет реального требования аудита изменений для MVP |

Побочное исправление: `User.telegram_id` — `unique=True` из `mapped_column` перенесено в явный `Index("ix_users_telegram_id", ..., unique=True)` в `User.__table_args__`. Это устраняет ложное обнаружение несоответствия при будущих autogenerate-запусках.

## Ревизия

Файл: `backend/alembic/versions/5dcbe7dd0861_schema_review_fixes.py`

```
Revision ID: 5dcbe7dd0861
Revises: 0001
```

Примечание: из авто-генерации удалены строки `drop_index(ix_users_telegram_id)` + `create_unique_constraint(None, users, [telegram_id])` — это не наши изменения, а Alembic-артефакт от смены `unique=True` → `Index` в модели; ревизия написана вручную с тремя реальными изменениями.

## Самопроверка

- [x] Три пункта применены (R-03, R-04, R-05)
- [x] R-07 зафиксирован как отложенный
- [x] `make backend-db-reset && make backend-db-migrate` — exit 0
- [x] `make backend-test` — 17 passed
- [x] `\d messages` → `ix_messages_dialogue_created` виден
- [x] `\d progress` → `uq_progress_student_period` виден
