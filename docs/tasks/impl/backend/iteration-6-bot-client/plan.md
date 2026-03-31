# Итерация 6 (Backend Tasklist): рефакторинг бота — план

**Статус:** завершена (см. [summary.md](summary.md))

## Цель

Перевести Telegram-бот в режим тонкого клиента: `POST /v1/dialogue/message`, без прямых вызовов LLM из процесса бота.

## Ценность

- Соответствие [docs/vision.md](../../../../vision.md): логика и LLM в backend.
- Один источник истины для диалога и истории (БД backend).

## Состав задач

| № (tasklist) | Задача | Документ |
|--------------|--------|----------|
| 14 | HTTP-клиент backend, удаление LLM из бота | [../tasks/task-14-bot-client/plan.md](../tasks/task-14-bot-client/plan.md) |
| 15 | Интеграционный smoke, README | [../tasks/task-15-integration-smoke/plan.md](../tasks/task-15-integration-smoke/plan.md) |

## Критерии завершения итерации

- В `src/` нет импорта `openai`.
- `make backend-test` — без регрессии.
- README содержит чеклист запуска backend + бот.
