# Итерация 4 (Backend): базовые API-тесты — summary

**Статус:** завершена ✅

## Итог

- `make backend-test` — **8 passed**, exit 0; тесты не требуют живой БД или реального LLM-ключа.
- Все проверки агентского чек-листа выполнены (см. [tasklist-backend.md](../../../tasklist-backend.md), Этап 4).

## Что реализовано

| Слой | Артефакт |
|------|----------|
| Dev-зависимости | `pytest`, `pytest-asyncio`, `httpx` в `backend/pyproject.toml` |
| Конфиг | `asyncio_mode=auto` в корневом `pyproject.toml`; `@pytest.mark.asyncio` не нужен |
| Команда | `make backend-test` |
| Изоляция | autouse-сброс `lru_cache` Settings и in-memory состояния stub |
| Фикстуры | `dialogue_client` — async, typed, mock LLM через `dependency_overrides`; в `conftest.py` |
| Тесты health | 1: `GET /health` без `DATABASE_URL` → 503 |
| Тесты диалога | 7: success, continuation, 422 (3 param), 404 |
| Stub-роутер | `POST /v1/dialogue/message` в `api/dialogue.py`; заменяется в задаче 13 |

## Отклонения

- Тесты диалога изначально планировались с `xfail` до задачи 13. Решение: stub-реализация введена в той же итерации, чтобы harness был зелёным с первого прогона. Контракт (URL, тело запроса/ответа) неизменен — задача 13 заменит только логику сервиса.

## Артефакты задач

| Задача | Summary |
|--------|---------|
| 08 | [task-08-test-harness/summary.md](../tasks/task-08-test-harness/summary.md) |
| 09 | [task-09-api-smoke-tests/summary.md](../tasks/task-09-api-smoke-tests/summary.md) |
