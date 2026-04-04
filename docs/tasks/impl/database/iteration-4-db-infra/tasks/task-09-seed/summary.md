# Задача 09 — Seed-скрипт: summary

**Дата:** 2026-04-04  
**Статус:** ✅ Done

## Что сделано

- Создан `backend/scripts/seed.py` — идемпотентный async-скрипт
- Цель `backend-db-seed` добавлена в `Makefile` и `.PHONY`

## Данные

| Сущность | Ключевые поля |
|----------|--------------|
| teacher | role=teacher, name="Преподаватель" |
| student | role=student, name="Ученик", telegram_id=111111111 |
| lesson | topic="Seed-занятие", status=scheduled, scheduled_at=завтра |
| assignment | description="Seed-задание: повторить пройденный материал", due_date=через неделю, status=pending |

`DEV_STUDENT_TELEGRAM_ID = 111111111` задокументирован в заголовке скрипта и в разделе 6 `db-guide.md`.

## Реализация

Скрипт создаёт движок напрямую через `create_async_engine(settings.database_url)` без использования приватных переменных `db.py`. Каждая сущность проверяется перед вставкой (`SELECT` по уникальному признаку).

## Отклонения от плана

Добавлен `import date` внутри функции `_get_or_create_assignment` — перемещён в топ модуля для чистоты (нет расхождений с поведением).

## Проверка

- Первый запуск: созданы 4 записи (teacher, student, lesson, assignment)
- Повторный запуск: все 4 уже существуют, `Seed complete.` без ошибок
- `SELECT count(*) FROM users;` → `2`
- `SELECT count(*) FROM lessons;` → `1`
- `SELECT count(*) FROM assignments;` → `1`
- `make lint` — `All checks passed!`
