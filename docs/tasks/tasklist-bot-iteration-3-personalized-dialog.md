# Bot · Итерация 3: Персонализированный диалог

## Обзор

Бот переходит на архитектуру тонкого клиента: вместо прямого вызова LLM обращается к backend API. Backend формирует контекст ученика из БД (занятия, ДЗ, история) и передаёт его в LLM. История диалога сохраняется в `Dialogue` / `Message`.

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

## Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Backend API: эндпоинт приёма сообщения и генерации ответа | 📋 Planned | [план](impl/bot/iteration-3-personalized-dialog/tasks/task-01-chat-endpoint/plan.md) \| [summary](impl/bot/iteration-3-personalized-dialog/tasks/task-01-chat-endpoint/summary.md) |
| 02 | Формирование контекста ученика для LLM | 📋 Planned | [план](impl/bot/iteration-3-personalized-dialog/tasks/task-02-context/plan.md) \| [summary](impl/bot/iteration-3-personalized-dialog/tasks/task-02-context/summary.md) |
| 03 | Сохранение истории в Dialogue / Message | 📋 Planned | [план](impl/bot/iteration-3-personalized-dialog/tasks/task-03-history/plan.md) \| [summary](impl/bot/iteration-3-personalized-dialog/tasks/task-03-history/summary.md) |
| 04 | Рефакторинг бота: удалить прямой вызов LLM, перейти на backend API | 📋 Planned | [план](impl/bot/iteration-3-personalized-dialog/tasks/task-04-bot-refactor/plan.md) \| [summary](impl/bot/iteration-3-personalized-dialog/tasks/task-04-bot-refactor/summary.md) |
