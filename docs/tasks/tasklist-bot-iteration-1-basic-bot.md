# Bot · Итерация 1: Базовый бот с LLM

## Обзор

Минимальный рабочий Telegram-бот на aiogram, принимающий сообщения ученика и отвечающий через OpenRouter (OpenAI-compatible API). Итерация закладывает структуру пакета `bot/`, конфигурацию и logging-инфраструктуру.

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Инициализация пакета bot/ и окружения | 📋 Planned | [план](impl/bot/iteration-1-basic-bot/tasks/task-01-init/plan.md) \| [summary](impl/bot/iteration-1-basic-bot/tasks/task-01-init/summary.md) |
| 02 | Конфиг через pydantic-settings + .env | 📋 Planned | [план](impl/bot/iteration-1-basic-bot/tasks/task-02-config/plan.md) \| [summary](impl/bot/iteration-1-basic-bot/tasks/task-02-config/summary.md) |
| 03 | Базовые хендлеры (/start, свободный текст) | 📋 Planned | [план](impl/bot/iteration-1-basic-bot/tasks/task-03-handlers/plan.md) \| [summary](impl/bot/iteration-1-basic-bot/tasks/task-03-handlers/summary.md) |
| 04 | LLM-сервис (прямой вызов OpenRouter) | 📋 Planned | [план](impl/bot/iteration-1-basic-bot/tasks/task-04-llm/plan.md) \| [summary](impl/bot/iteration-1-basic-bot/tasks/task-04-llm/summary.md) |
| 05 | Logging и запуск через Makefile | 📋 Planned | [план](impl/bot/iteration-1-basic-bot/tasks/task-05-logging-make/plan.md) \| [summary](impl/bot/iteration-1-basic-bot/tasks/task-05-logging-make/summary.md) |
