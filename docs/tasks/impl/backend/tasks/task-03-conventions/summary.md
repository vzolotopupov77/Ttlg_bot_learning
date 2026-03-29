# Задача 03: Обновить `.cursor/rules/conventions.mdc` — summary

## Сделано

- Обновлён [.cursor/rules/conventions.mdc](../../../../../../.cursor/rules/conventions.mdc):
  - В **Стек** добавлена строка про backend (FastAPI, PostgreSQL, SQLAlchemy async, Alembic) со ссылками на vision и ADR.
  - Секция **Telegram-бот:** целевой поток через HTTP backend; явно про «тонкий клиент» и временные LLM-вызовы до миграции.
  - Новая секция **Backend (ядро):** пакет `backend/src/ttlg_backend/`, слои, async, Depends, тесты (`make backend-test`, pytest + httpx), правило про Makefile.
  - Frontmatter `description`: «бот + backend».

## Отклонения

- Нет.

## Проверка

- Стек не шире, чем в [docs/vision.md](../../../../../vision.md).
