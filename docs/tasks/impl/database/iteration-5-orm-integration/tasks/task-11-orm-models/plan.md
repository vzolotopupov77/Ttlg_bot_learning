# Задача 11: Актуализация ORM-моделей — план

**Дата:** 2026-04-05

## Цель

Применить решения из summary задачи 05 (ревью схемы): добавить недостающие индексы и UniqueConstraint; создать новую Alembic-ревизию.

## Изменения

Источник: `docs/tasks/impl/database/iteration-2-schema-design/tasks/task-05-schema-review/summary.md`, раздел «Для задачи 11».

| Пункт | Изменение в models.py |
|-------|----------------------|
| R-04 | `Index("ix_messages_dialogue_created", "dialogue_id", "created_at")` на `Message.__table_args__` |
| R-05 | `Index("ix_lessons_scheduled_at", "scheduled_at")` на `Lesson.__table_args__` |
| R-03 | `UniqueConstraint("student_id", "period_start", "period_end", name="uq_progress_student_period")` на `Progress.__table_args__` |
| R-07 | `updated_at` — отложить (нет требования аудита в MVP) |

Побочно: `User.telegram_id` — заменить `unique=True` в `mapped_column` на явный `Index("ix_users_telegram_id", "telegram_id", unique=True)` в `__table_args__`, чтобы устранить постоянное несоответствие при autogenerate.

## Файлы

- `backend/src/ttlg_backend/storage/models.py`
- `backend/alembic/versions/5dcbe7dd0861_schema_review_fixes.py`
