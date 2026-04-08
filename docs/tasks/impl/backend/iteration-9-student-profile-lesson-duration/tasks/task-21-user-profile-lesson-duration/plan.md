# Задача 21: профиль ученика и duration у занятия

## Изменения

- `docs/data-model.md`: User +3 поля, Lesson + `duration_minutes`, ER и физическая схема, constraint CHECK.
- `backend/src/ttlg_backend/storage/models.py`, новая миграция Alembic.
- `storage/repositories/users.py`, `lessons.py`; `api/users.py`, `api/lessons.py`.
- `backend/tests/test_crud_smoke.py`.
- Доки: `api-contracts.md`, `integrations.md`, `user-scenarios.md`, `vision.md`.
- `backend/pyproject.toml`: `email-validator`.

## DoD

- Миграция применима к PostgreSQL; ORM совпадает с `data-model.md`.
- OpenAPI через код обновляется автоматически при запуске приложения.
