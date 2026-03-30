# Задача 07: Summary

## Сделано

- [backend/src/ttlg_backend/config.py](../../../../../../backend/src/ttlg_backend/config.py): `Settings` (pydantic-settings), `DATABASE_URL` с валидацией схемы `postgresql+asyncpg://`, опциональный `OPENROUTER_API_KEY` как `SecretStr`, `LLM_MODEL`, `LOG_LEVEL`, `OPENROUTER_BASE_URL`.
- [backend/src/ttlg_backend/db.py](../../../../../../backend/src/ttlg_backend/db.py): async engine, `async_sessionmaker`, `ping_db()`, `get_session()`, `init_db` / `close_db`.
- [backend/src/ttlg_backend/logging.py](../../../../../../backend/src/ttlg_backend/logging.py): `setup_logging(level)`.
- [backend/src/ttlg_backend/main.py](../../../../../../backend/src/ttlg_backend/main.py): lifespan — логирование, инициализация БД, предупреждение если ping при старте не прошёл; shutdown — `dispose` engine.
- [.env.example](../../../../../../.env.example): блок backend с `DATABASE_URL` и комментариями.
- [docker-compose.yml](../../../../../../docker-compose.yml): PostgreSQL 16 Alpine, пользователь/БД `ttlg`, healthcheck; цель `make backend-db-up`.
- [README.md](../../../../../../README.md): раздел запуска backend и порт 8000.

## Безопасность логов

- При ошибке БД в лог пишется только имя типа исключения (`Database ping failed: …`), не `DATABASE_URL` и не `SecretStr`.

## Проверка

- `TestClient`: при недоступной БД `GET /health` → **503**, тело `degraded`.
- При запущенном Postgres с корректным `DATABASE_URL` ожидается **200** и `{"status":"ok"}`.
