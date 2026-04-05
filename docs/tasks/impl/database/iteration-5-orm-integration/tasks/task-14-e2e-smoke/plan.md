# Задача 14: End-to-end smoke на PostgreSQL + документация — план

**Дата:** 2026-04-05

## Цель

Верифицировать полный сценарий на PostgreSQL: reset → migrate → seed → run → POST → psql verify. Обновить документацию.

## Сценарий верификации

1. `make backend-db-reset && make backend-db-migrate && make backend-db-seed`
2. `make backend-run`
3. `POST /v1/dialogue/message` с `telegram_id=111111111` → ответ получен
4. `SELECT role, content FROM messages ORDER BY created_at DESC LIMIT 2;` → 2 строки

## Документация

- `README.md` — PostgreSQL как основной маршрут; SQLite с пометкой «только без Docker»
- `docs/vision.md` — проверить наличие «без PostgreSQL» пометок
- `docs/plan.md` — Итерация 2 PostgreSQL-часть (уже Done)
- `docs/tasks/tasklist-database.md` — статусы задач 11–14 → Done
