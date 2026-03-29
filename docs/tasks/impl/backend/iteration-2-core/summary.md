# Итерация 2 (Backend Core): summary — этап 1

## Статус

Этап 1 tasklist’а («Выбор стека и фиксация конвенций») завершён: задачи 01–03 — ✅ Done.

## Сделано

- [docs/vision.md](../../../../vision.md): зафиксированы FastAPI, PostgreSQL, расширенная таблица технологий, ссылки на ADR-001/002.
- [docs/adr/adr-002-orm-migrations-tests.md](../../../../adr/adr-002-orm-migrations-tests.md): ORM (SQLAlchemy async), Alembic, pytest + httpx + pytest-asyncio.
- [.cursor/rules/conventions.mdc](../../../../../.cursor/rules/conventions.mdc): секция Backend и уточнения по боту как тонкому клиенту.
- Планы и summary задач: [task-01](../tasks/task-01-stack/), [task-02](../tasks/task-02-adr-orm-tests/), [task-03](../tasks/task-03-conventions/).

## Отклонения

- Нет. Зависимости backend и `dev` зафиксированы в [pyproject.toml](../../../../../pyproject.toml) в рамках задачи 01.

## Следующее

Этап 2 [tasklist-backend.md](../../tasklist-backend.md): задачи 04–05 (контракт API и конвенции HTTP).
