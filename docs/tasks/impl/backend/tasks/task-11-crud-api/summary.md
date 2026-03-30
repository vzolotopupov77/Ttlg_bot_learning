# Задача 11: CRUD API — summary

**Статус:** завершена

## Итог

- Реализованы роуты под префиксом `/v1` (см. plan.md).
- Репозитории без тяжёлого DI; `AsyncSession` через `Depends(get_session)`.
- Прогресс: `GET /v1/users/{id}/progress` — live-агрегация по `lessons` / `assignments` (таблица `progress` не обязательна для этого эндпоинта).
- Тесты: `test_crud_smoke.py` (4 сценария).

## Замечания

- Ролевая проверка в эндпоинтах не реализована — только placeholder `require_auth`.
