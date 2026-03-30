# Итерация 4 (Backend): базовые API-тесты — план

**Статус плана:** выполнен — см. [summary.md](summary.md).

## Этап 4 — Базовые API-тесты

### Цель

Ввести **pytest** + **httpx.AsyncClient** по [ADR-002](../../../../adr/adr-002-orm-migrations-tests.md), добавить `make backend-test`, написать smoke по `GET /health` и контрактные тесты для `POST /v1/dialogue/message` согласно [api-contracts.md](../../../../tech/api-contracts.md).

### Ценность

Единая команда проверки backend; регрессия по контракту диалога фиксируется тестами до и параллельно с реализацией эндпоинта (задача 13).

### Задачи

| Задача | Описание | Артефакты |
|--------|-----------|-----------|
| 08 | Окружение pytest, фикстуры, `backend-test` | [task-08](../tasks/task-08-test-harness/), `backend/tests/`, `Makefile`, dev-deps в `backend/pyproject.toml` |
| 09 | Smoke по сценарию сообщений (контракт + негативы) | [task-09](../tasks/task-09-api-smoke-tests/), `backend/tests/test_dialogue.py` |

### Состав артефактов (целевой)

| Область | Файлы |
|---------|--------|
| Зависимости | [backend/pyproject.toml](../../../../../backend/pyproject.toml) — `[project.optional-dependencies] dev`: `pytest`, `pytest-asyncio`, `httpx` |
| Тесты | `backend/tests/conftest.py`, `test_health.py`, `test_dialogue.py` (после задачи 09) |
| Запуск | [Makefile](../../../../../Makefile): цель `backend-test` (`uv run --package ttlg-backend pytest …`) |
| Контракт | [docs/tech/api-contracts.md](../../../../tech/api-contracts.md), [docs/api-conventions.md](../../../../api-conventions.md) |

### Критерии готовности (DoD этапа)

- `make backend-test` завершается с кодом **0**.
- Есть минимум один стабильный тест на `/health` (assert на ожидаемый код и тело в тестовой конфигурации env).
- Для диалога — тесты по контракту (успех с mock LLM, 422, 404); до реализации роутера в задаче 13 допускается согласованная пометка ожидаемого падения (см. план задачи 09).
- Способ mock LLM описан в плане задачи 09 или в комментарии к фикстуре.

### Самопроверка перед закрытием

См. раздел **«Проверка этапа 4»** в [tasklist-backend.md](../../../tasklist-backend.md).

---

## Ссылка на tasklist

[docs/tasks/tasklist-backend.md](../../../tasklist-backend.md) — этап 4 (задачи 08–09).

## Предыдущий контекст

Итерация 3 (каркас): [iteration-3-scaffold](../iteration-3-scaffold/summary.md).

## Итог

После выполнения реализации — `summary.md` в этой папке и `summary.md` у задач 08–09.
