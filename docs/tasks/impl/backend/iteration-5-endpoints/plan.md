# Итерация 5 (Backend): эндпоинты и серверная логика — план

**Статус:** завершена (см. [summary.md](summary.md))

## Цель

Реализовать персистентный домен (ORM + миграции), базовый CRUD API, LLM-клиент (OpenRouter) и полный сценарий `POST /v1/dialogue/message` с сохранением истории в БД вместо stub.

## Ценность

- Данные ученика, занятий, ДЗ и диалогов хранятся в PostgreSQL.
- Клиенты (бот, веб) получают единый контракт из [api-contracts.md](../../../tech/api-contracts.md).
- Регрессия по smoke-тестам диалога сохраняется.

## Состав задач

| № | Задача | Зависимости |
|---|--------|-------------|
| 10 | ORM-модели + Alembic | — |
| 11 | CRUD API (users, lessons, assignments, progress read) | 10 |
| 12 | LLM-клиент + промпт | 10 (конфиг/слой), логически независим от 11 |
| 13 | Эндпоинт диалога (БД + LLM, удаление stub) | 10, 11, 12 |

## Критерии завершения итерации

- `alembic upgrade head` на чистой БД успешен (`make backend-db-migrate`).
- `make backend-test` — все тесты зелёные, в т.ч. диалог с тестовой БД и моком LLM.
- Таблицы `users`, `lessons`, `assignments`, `progress`, `dialogues`, `messages` созданы миграцией.
- OpenAPI (`/docs`) содержит новые роуты CRUD.

## Артефакты задач

| Задача | План | Summary |
|--------|------|---------|
| 10 | [task-10-orm-migrations/plan.md](../tasks/task-10-orm-migrations/plan.md) | (по завершении) |
| 11 | [task-11-crud-api/plan.md](../tasks/task-11-crud-api/plan.md) | (по завершении) |
| 12 | [task-12-llm/plan.md](../tasks/task-12-llm/plan.md) | (по завершении) |
| 13 | [task-13-dialogue-endpoint/plan.md](../tasks/task-13-dialogue-endpoint/plan.md) | (по завершении) |
