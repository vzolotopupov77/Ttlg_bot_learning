# Задача 11: CRUD API — план

## Цель

Базовые HTTP-операции для `User`, `Lesson`, `Assignment` и агрегированный прогресс ученика.

## Роуты (префикс `/v1`)

| Метод | Путь | Назначение |
|-------|------|------------|
| POST | `/users` | Создать пользователя |
| GET | `/users/{user_id}` | Получить пользователя |
| GET | `/users/{user_id}/progress` | Сводка по урокам/ДЗ (агрегация) |
| POST | `/lessons` | Создать занятие |
| GET | `/lessons/{lesson_id}` | Получить занятие |
| PATCH | `/lessons/{lesson_id}/status` | Обновить статус |
| POST | `/assignments` | Создать ДЗ |
| GET | `/assignments/{assignment_id}` | Получить ДЗ |
| PATCH | `/assignments/{assignment_id}/status` | Обновить статус |

## Слои

- Роутеры: `api/users.py`, `api/lessons.py`, `api/assignments.py`
- Репозитории: `storage/repositories/*`
- Авторизация: `dependencies.require_auth` — заглушка

## Тесты

- `backend/tests/test_crud_smoke.py` на SQLite (см. `TTLG_ALLOW_SQLITE_TEST` + in-memory URL в фикстурах).
