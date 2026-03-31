# Задача 15: интеграционный smoke — summary

**Статус:** ✅ Done

## Сделано

- В [README.md](../../../../../README.md) добавлен раздел **End-to-end: бот → backend → LLM** с пошаговым чеклистом (БД, миграции, регистрация пользователя, два терминала, Telegram).
- В [Makefile](../../../../../Makefile) цель `smoke-integration` — печать того же чеклиста.

## Проверки

- Упомянутые команды (`make backend-db-up`, `make backend-db-migrate`, `make backend-run`, `make run`) присутствуют в Makefile.
- `make backend-test` — без регрессии.
