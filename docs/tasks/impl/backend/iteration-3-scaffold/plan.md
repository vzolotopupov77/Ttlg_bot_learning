# Итерация 3 (Backend): каркас сервиса — план

**Статус плана:** выполнен (реализация зафиксирована в [summary.md](summary.md)).

## Этап 3 — Каркас backend-сервиса

### Цель

Поднять пакет `ttlg_backend` (uv workspace member), FastAPI-приложение с проверкой готовности `/health`, конфигурацию через **pydantic-settings**, async-подключение к PostgreSQL и структурированное логирование без утечки секретов.

### Ценность

Локальный запуск backend одной командой из Makefile; единый контур настройки и БД для этапов 4–5 (тесты, ORM, эндпоинт диалога).

### Задачи

| Задача | Описание | Артефакты |
|--------|-----------|-----------|
| 06 | Каркас, `/health` | [task-06](../tasks/task-06-scaffold/), `backend/`, Makefile |
| 07 | Конфиг, БД, логи | [task-07](../tasks/task-07-config-db-logging/), `.env.example`, `docker-compose.yml` |

### Состав артефактов (фактический)

| Область | Файлы |
|---------|--------|
| Workspace | Корневой [pyproject.toml](../../../../../pyproject.toml) — `[tool.uv.workspace]`, member `backend` |
| Пакет backend | [backend/pyproject.toml](../../../../../backend/pyproject.toml), [backend/src/ttlg_backend/](../../../../../backend/src/ttlg_backend/) (`main`, `config`, `db`, `logging`) |
| Запуск | [Makefile](../../../../../Makefile): `install`, `backend-install`, `backend-run`, `backend-db-up` |
| Инфра | [docker-compose.yml](../../../../../docker-compose.yml) (PostgreSQL 16) |
| Env | [.env.example](../../../../../.env.example) — `DATABASE_URL` и комментарии |
| Документация | [README.md](../../../../../README.md) — раздел Backend |

### Критерии готовности (DoD этапа)

- `make backend-install` / `make install` завершаются успешно (`uv sync --all-packages`).
- `make backend-run` поднимает API на **127.0.0.1:8000**.
- `GET /health`: **200** и `{"status":"ok"}` при доступной БД; **503** и `degraded` при недоступной.
- Неверная схема `DATABASE_URL` (не `postgresql+asyncpg://`) — отказ при валидации **без** утечки пароля.
- В логах при ошибке БД — тип исключения, не полный URL с паролем.

### Самопроверка перед закрытием

- [ ] Импорт: `uv run --package ttlg-backend python -c "from ttlg_backend.main import app"`.
- [ ] Без Postgres: `GET /health` → 503.
- [ ] С Postgres и валидным `DATABASE_URL`: `GET /health` → 200.
- [ ] В `tasklist-backend.md` задачи 06–07 — ✅ Done; планы/summary задач не битые.

---

## Ссылка на tasklist

[docs/tasks/tasklist-backend.md](../../../tasklist-backend.md) — этап 3 (задачи 06–07).

## Следующие шаги (вне этапа 3)

Этап 4: pytest, `make backend-test`, smoke API (задачи 08–09).

## Итог

После выполнения — [summary.md](summary.md).
