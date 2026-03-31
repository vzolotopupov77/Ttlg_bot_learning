# Итерация 7 (Backend Tasklist): документирование — план

**Статус:** завершена (см. [summary.md](summary.md)).

## Цель

Закрыть документирование backend: OpenAPI (`/docs`), полнота `.env.example`, синхронизация README/plan/vision/integrations с фактическим состоянием после этапов 1–6.

## Ценность

- Клиенты и разработчики ориентируются по Swagger без чтения кода.
- Один эталон переменных окружения для бота и backend.
- Продуктовая документация не расходится с репозиторием.

## Состав задач

| № (tasklist) | Задача | Документ |
|--------------|--------|----------|
| 16 | OpenAPI `/docs`, описания схем | [../tasks/task-16-openapi-docs/plan.md](../tasks/task-16-openapi-docs/plan.md) |
| 17 | `.env.example`: все переменные | [../tasks/task-17-env-example/plan.md](../tasks/task-17-env-example/plan.md) |
| 18 | README, vision, plan, integrations | [../tasks/task-18-docs-sync/plan.md](../tasks/task-18-docs-sync/plan.md) |

## Критерии завершения итерации

- `make backend-test` — зелёный.
- `/docs`: 4 тега + `/health`, у операций заданы `summary`.
- `.env.example` покрывает `Settings` и бот-конфиг.
- README/plan/vision/integrations согласованы с Makefile и кодом.
