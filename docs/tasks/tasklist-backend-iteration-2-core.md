# Backend · Итерация 2: Backend Core

## Обзор

FastAPI-сервис с PostgreSQL и базовыми CRUD-эндпоинтами для всех доменных сущностей (`User`, `Lesson`, `Assignment`, `Progress`, `Dialogue`, `Message`). Итерация закладывает структуру пакета `backend/`, миграции и конфигурацию.

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Инициализация пакета backend/ и окружения | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-01-init/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-01-init/summary.md) |
| 02 | Конфиг через pydantic-settings (DATABASE_URL, etc.) | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-02-config/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-02-config/summary.md) |
| 03 | Доменная модель и миграции (все сущности) | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-03-domain/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-03-domain/summary.md) |
| 04 | CRUD-эндпоинты FastAPI | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-04-api/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-04-api/summary.md) |
| 05 | Smoke-тесты и запуск через Makefile | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-05-tests-make/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-05-tests-make/summary.md) |
