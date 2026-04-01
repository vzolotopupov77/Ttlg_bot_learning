# Итерация 8 (Backend Tasklist): качество и инженерные практики — план

**Статус:** завершена (см. [summary.md](summary.md)).

## Цель

Ввести единый линт/формат (Ruff + Makefile), убедиться в таймаутах и fallback для внешних вызовов, зафиксировать правила логирования без утечек секретов; зафиксировать выбор инструментов качества в ADR и conventions; расширить самопроверки этапа 8 в тасклисте.

## Ценность

- Одинаковый стиль кода в монорепо (бот + backend).
- Предсказуемое поведение при сбоях сети и LLM.
- Проверки перед PR сводятся к целям Makefile.
- Dev-окружение воспроизводимо после одной команды `uv sync`.
- Решения по инструментам зафиксированы в ADR — основание для будущих изменений.

## Состав задач

| № (tasklist) | Задача | Документ |
|--------------|--------|----------|
| 19 | Ruff, `make lint` / `format` / `check` | [../tasks/task-19-lint-format/plan.md](../tasks/task-19-lint-format/plan.md) |
| 20 | Таймауты, fallback, логи | [../tasks/task-20-resilience-logging/plan.md](../tasks/task-20-resilience-logging/plan.md) |
| — | ADR-003: выбор инструментов качества | [docs/adr/adr-003-quality-tooling.md](../../../../adr/adr-003-quality-tooling.md) |

## Критерии завершения итерации

- `make lint`, `make check` — без ошибок.
- `make backend-test`, `make bot-test` — зелёные.
- Dev-зависимости перенесены в `[dependency-groups]`; `default-groups` настроен.
- ADR-003 зафиксирован; `conventions.mdc` обновлён.
- Блок «Проверка этапа 8» в `tasklist-backend.md` заполнен самопроверками; статусы задач 19–20 — Done.
