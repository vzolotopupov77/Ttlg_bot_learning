# Backend — ttlg-backend

FastAPI-сервер: бизнес-логика, REST API, LLM-контекст, PostgreSQL.

По умолчанию слушает **http://127.0.0.1:8000**.

## Быстрый старт

```bash
# Из корня репозитория
cp .env.example .env          # задайте DATABASE_URL, SECRET_KEY, OPENROUTER_API_KEY
make install                   # uv sync --all-packages

make backend-db-up             # PostgreSQL в Docker (localhost:5432)
make backend-db-migrate        # Alembic: применить миграции
make backend-db-seed           # создать тестового преподавателя и ученика
make backend-run               # http://127.0.0.1:8000
```

Проверка готовности: `GET http://127.0.0.1:8000/health` → `{"status":"ok"}`.

Swagger UI: `http://127.0.0.1:8000/docs`.

## Тесты

```bash
make backend-db-test-create    # однократно: CREATE DATABASE ttlg_test
make backend-test              # pytest backend/tests -v
```

Тесты требуют PostgreSQL (`ttlg_test`). LLM замокан.

## Структура

```
backend/
├── src/ttlg_backend/
│   ├── main.py          # точка входа FastAPI
│   ├── config.py        # pydantic-settings, читает .env
│   ├── db.py            # AsyncEngine, AsyncSession
│   ├── dependencies.py  # Depends-зависимости
│   ├── api/             # роутеры по ресурсам (auth, users, lessons, …)
│   ├── services/        # бизнес-логика (auth_service, dialogue_service)
│   ├── storage/         # ORM-модели, репозитории
│   └── llm/             # OpenAI-compatible клиент к OpenRouter
├── alembic/             # миграции
├── scripts/seed.py      # загрузка тестовых данных
├── tests/               # pytest + httpx AsyncClient
└── alembic.ini
```

## Переменные окружения

Все переменные описаны в [`.env.example`](../.env.example). Ключевые для backend:

| Переменная | Обязательна | Описание |
|------------|-------------|----------|
| `DATABASE_URL` | да | `postgresql+asyncpg://ttlg:ttlg@127.0.0.1:5432/ttlg` |
| `SECRET_KEY` | да | JWT-секрет, не коммитить |
| `OPENROUTER_API_KEY` | для LLM | ключ [openrouter.ai](https://openrouter.ai/keys) |
| `DATABASE_TEST_URL` | для тестов | `postgresql+asyncpg://ttlg:ttlg@127.0.0.1:5432/ttlg_test` |

## Дополнительные команды

```bash
make backend-db-reset          # сбросить БД и накатить миграции заново
make backend-db-shell          # psql в контейнере
make backend-db-logs           # логи PostgreSQL
make openapi-export            # сгенерировать docs/openapi.json
```

## Документация

- [HTTP API контракты](../docs/tech/api-contracts.md)
- [Модель данных](../docs/data-model.md)
- [Практическая справка по БД](../docs/tech/db-guide.md)
- [ADR: база данных](../docs/adr/adr-001-database.md)
