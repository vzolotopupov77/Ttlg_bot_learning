# Задача 09 — Seed-скрипт: план

**Итерация:** 4  
**Дата:** 2026-04-04  
**Статус:** In Progress

## Цель

Создать идемпотентный скрипт тестового наполнения БД: один преподаватель, один ученик с известным `telegram_id`, одно занятие, одно ДЗ.

## Затрагиваемые файлы

| Файл | Изменение |
|------|-----------|
| `backend/scripts/seed.py` | Создать |
| `Makefile` | Добавить цель `backend-db-seed` |

## Данные для seed

| Сущность | Ключевые поля |
|----------|--------------|
| teacher | role=teacher, name="Преподаватель" |
| student | role=student, name="Ученик", telegram_id=`DEV_STUDENT_TELEGRAM_ID` (константа) |
| lesson | student=student, teacher=teacher, topic="Seed-занятие", status=scheduled, scheduled_at=завтра |
| assignment | student=student, lesson=lesson, description="Seed-задание", due_date=через неделю, status=pending |

`DEV_STUDENT_TELEGRAM_ID = 111111111` — dev-константа, задокументирована в скрипте и `db-guide.md`.

## Идемпотентность

- teacher: `SELECT` по `name = "Преподаватель"` AND `role = teacher`
- student: существующий `get_student_by_telegram_id(DEV_STUDENT_TELEGRAM_ID)`
- lesson: `SELECT` по `topic = "Seed-занятие"` AND `student_id`
- assignment: `SELECT` по `lesson_id` AND `student_id`

## Реализация

Скрипт создаёт движок напрямую через `create_async_engine(settings.database_url)` — не зависит от приватных переменных `db.py`.

```makefile
backend-db-seed:
	uv run --package ttlg-backend python backend/scripts/seed.py
```

## Самопроверка

- `make backend-db-seed` завершается без ошибок, выводит `Seed complete.`
- Повторный запуск: `SELECT count(*) FROM users;` → `2`
- `SELECT count(*) FROM lessons;` → `1`, `SELECT count(*) FROM assignments;` → `1`
- `make lint` — без ошибок
