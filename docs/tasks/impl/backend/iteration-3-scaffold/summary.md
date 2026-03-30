# Итерация 3 (Backend): каркас сервиса — summary

**Дата закрытия этапа:** 2026-03-30  
**Статус:** этап 3 (задачи 06–07) завершён.

## Результат

- **uv workspace:** корень + [backend/](../../../../../backend/), пакет **`ttlg-backend`** (`ttlg_backend` в коде).
- **FastAPI:** [main.py](../../../../../backend/src/ttlg_backend/main.py) — `lifespan` (логи, init/dispose БД), **`GET /health`**: при успешном `SELECT 1` — **200** `{"status":"ok"}`; иначе — **503** `{"status":"degraded","database":"unavailable"}`.
- **Конфиг:** [config.py](../../../../../backend/src/ttlg_backend/config.py) — `DATABASE_URL` (только `postgresql+asyncpg://`), LLM/OpenRouter-поля, `LOG_LEVEL`; `OPENROUTER_API_KEY` опционален до эндпоинтов LLM.
- **БД:** [db.py](../../../../../backend/src/ttlg_backend/db.py) — async engine, `get_session`, `ping_db`.
- **Логи:** [logging.py](../../../../../backend/src/ttlg_backend/logging.py).

Детализация по задачам: [06](../tasks/task-06-scaffold/summary.md), [07](../tasks/task-07-config-db-logging/summary.md).

## Команды

| Команда | Назначение |
|---------|------------|
| `make install` / `make backend-install` | `uv sync --all-packages` |
| `make backend-run` | uvicorn **127.0.0.1:8000**, `--reload` |
| `make backend-db-up` | `docker compose up -d db` (Postgres 16) |

## Отклонения от формулировок в tasklist

- **503 без БД** считается ожидаемым поведением до поднятия PostgreSQL; «всегда 200» на `/health` в DoD не требуется.
- **`make install`** синхронизирует весь workspace (бот + backend), не только один пакет.

## Проверка структуры (ориентир)

Сверка с skill *fastapi-templates*: async lifespan, async routes, pydantic-settings, async SQLAlchemy — соблюдены. Каталоги `api/`, `services/`, `storage/`, `llm/` из [vision.md](../../../../vision.md) — **на этапе 5+**, после ORM и доменных роутов.

## Следующий этап в tasklist

**Этап 4:** задачи **08–09** — pytest, `make backend-test`, smoke по HTTP API.
