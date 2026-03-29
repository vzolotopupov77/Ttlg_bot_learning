# Итерация 2 (Backend Core): summary

## Статус (этап 1)

Этап 1 tasklist’а («Выбор стека и фиксация конвенций») завершён: задачи 01–03 — ✅ Done.

## Сделано

- [docs/vision.md](../../../../vision.md): зафиксированы FastAPI, PostgreSQL, расширенная таблица технологий, ссылки на ADR-001/002.
- [docs/adr/adr-002-orm-migrations-tests.md](../../../../adr/adr-002-orm-migrations-tests.md): ORM (SQLAlchemy async), Alembic, pytest + httpx + pytest-asyncio.
- [.cursor/rules/conventions.mdc](../../../../../.cursor/rules/conventions.mdc): секция Backend и уточнения по боту как тонкому клиенту.
- Планы и summary задач: [task-01](../tasks/task-01-stack/), [task-02](../tasks/task-02-adr-orm-tests/), [task-03](../tasks/task-03-conventions/).

## Отклонения

- Нет. Зависимости backend и `dev` зафиксированы в [pyproject.toml](../../../../../pyproject.toml) в рамках задачи 01.

## Этап 2 — Проектирование API-контракта

**Статус:** задачи 04–05 — ✅ Done.

**Сделано:**

- [docs/api-conventions.md](../../../../api-conventions.md): префикс `/v1`, формат `error`, таблица HTTP, заглушка `X-User-Role`, нормализация `422` (`RequestValidationError` → единый `error`).
- [docs/integrations.md](../../../../integrations.md): раздел **Backend HTTP API** (сводка `POST /v1/dialogue/message`), ссылки на `api-conventions.md` и `api-contracts.md`.
- [docs/tech/api-contracts.md](../../../../tech/api-contracts.md): полный контракт диалога — заголовки, поля, примеры, таблица ошибок, заметки по дизайну (URL-иерархия, идемпотентность).
- Планы и summary: [task-04](../tasks/task-04-api-dialogue-contract/), [task-05](../tasks/task-05-api-conventions/).

**Дополнительно:** пройдена проверка `api-design-principles`; выявленные замечания (стык 422, безопасность dialogue_id, заголовки, future notes) устранены или задокументированы.

## Следующее

Этап 3 [tasklist-backend.md](../../tasklist-backend.md): задачи 06–07 (каркас FastAPI, конфиг и БД).
