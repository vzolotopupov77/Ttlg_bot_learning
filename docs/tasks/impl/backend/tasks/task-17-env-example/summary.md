# Задача 17: `.env.example` — summary

**Статус:** завершена.

## Сделано

- Секции «бот» и «backend»; переменные: `TELEGRAM_BOT_TOKEN`, `BACKEND_URL`, `BACKEND_TIMEOUT`, `DATABASE_URL`, `OPENROUTER_*`, `LLM_*`, `LOG_LEVEL`, закомментированный `TTLG_ALLOW_SQLITE_TEST`.
- Комментарий про незаданный `DATABASE_URL` и degraded `/health`.

## Ручная проверка

- Старт backend и бота по `.env` из примера (SQLite) — ок.

## Отклонения

- Нет.
