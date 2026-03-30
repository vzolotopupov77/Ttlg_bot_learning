# Задача 07: Конфиг, async PostgreSQL, логирование

## Цель

Настроить `pydantic-settings` для backend (`DATABASE_URL`, OpenRouter/LLM, уровень логов), async engine SQLAlchemy + session factory, инициализацию в lifespan с проверкой `SELECT 1`, структурированные логи без вывода пароля и API-ключей в открытом виде.

## Что меняется

- `backend/src/ttlg_backend/config.py`: класс `Settings`.
- `backend/src/ttlg_backend/db.py`: `create_async_engine`, `async_sessionmaker`, `get_session`, `init_db` / `close_db` или эквивалент.
- `backend/src/ttlg_backend/logging.py`: `setup_logging(level: str)`.
- `backend/src/ttlg_backend/main.py`: lifespan, флаг / готовность БД в `app.state`, `/health` возвращает 503 при недоступности БД.
- [.env.example](../../../../../../.env.example): `DATABASE_URL` и комментарии к backend-переменным.
- Опционально: [docker-compose.yml](../../../../../../docker-compose.yml) и цель `make backend-db-up`.
- [README.md](../../../../../../README.md): команды backend и порт.

## Definition of Done

- С валидным `.env` и запущенной PostgreSQL приложение стартует; `/health` → 200.
- При недоступной БД — WARNING в логе (без пароля из URL); `/health` → 503.
- Неверный формат `DATABASE_URL` при старте — понятная ошибка до вывода секретов.

## Документы

- Summary: [summary.md](summary.md)
