# Итерация 2 (Backend Core): план

## Этап 1 — Выбор стека и фиксация конвенций

### Цель

Зафиксировать backend-стек, задокументировать решения по ORM/миграциям/тестам (ADR), обновить правила Cursor под единый стек.

### Ценность

Единый источник правды для реализации этапов 2–8 tasklist’а; нет расхождений между `vision.md`, ADR и `conventions.mdc`.

### Задачи

| Задача | Описание | Артефакты |
|--------|-----------|-----------|
| 01 | Backend-стек | [docs/vision.md](../../../../vision.md), [task-01](../tasks/task-01-stack/) |
| 02 | ADR ORM, миграции, тесты | [ADR-002](../../../../adr/adr-002-orm-migrations-tests.md), [task-02](../tasks/task-02-adr-orm-tests/) |
| 03 | Конвенции Cursor | [.cursor/rules/conventions.mdc](../../../../../.cursor/rules/conventions.mdc), [task-03](../tasks/task-03-conventions/) |

---

## Этап 2 — Проектирование API-контракта

### Цель

Зафиксировать черновик контракта диалога (`POST /v1/dialogue/message`) и единые конвенции HTTP API для клиентов бота и веба.

### Ценность

Реализация этапов 3–5 и smoke-тесты опираются на согласованный контракт и формат ошибок без расхождений между документами.

### Задачи

| Задача | Описание | Артефакты |
|--------|-----------|-----------|
| 04 | Контракт диалога | [task-04](../tasks/task-04-api-dialogue-contract/), [docs/integrations.md](../../../../integrations.md) |
| 05 | Конвенции API | [task-05](../tasks/task-05-api-conventions/), [docs/api-conventions.md](../../../../api-conventions.md) |

### Следующие шаги (вне этапа 2)

Этап 3 tasklist’а: каркас FastAPI, `/health`, конфиг и БД (задачи 06–07).

---

## Ссылка на tasklist

[docs/tasks/tasklist-backend.md](../../tasklist-backend.md) — этапы 1–2.
