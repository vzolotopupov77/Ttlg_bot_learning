# Итерация 8 — Тестирование: summary

## Статус

Завершена: ручные чек-листы зафиксированы; автотесты подключены; `make frontend-test` проходит (15 тестов). Пользователь подтвердил `make frontend-test` и `make check` (2026-04-22).

## Задача 24

- Чек-листы по 5 экранам: [`tasks/task-24-test-scenarios/summary.md`](./tasks/task-24-test-scenarios/summary.md).
- План задачи: [`tasks/task-24-test-scenarios/plan.md`](./tasks/task-24-test-scenarios/plan.md).
- Ручная приёмка: ключевые сценарии (≥5) пройдены пользователем — см. раздел «Приёмка пользователя» в summary задачи 24 (2026-04-22).

## Задача 25

- Отчёт: [`tasks/task-25-automated-tests/summary.md`](./tasks/task-25-automated-tests/summary.md).
- План: [`tasks/task-25-automated-tests/plan.md`](./tasks/task-25-automated-tests/plan.md).

## Команды для пользователя

1. Ручная приёмка: открыть чек-листы и пройти ≥5 ключевых сценариев в браузере при работающем `make frontend-dev` и backend. (Выполнено.)
2. `make frontend-test` — все тесты зелёные. (Выполнено.)
3. `make check` — общий пайплайн репозитория. (Выполнено.)

## Примечания

- В `frontend/tsconfig.json` не добавлялся `types: ["vitest/globals"]`, чтобы не сужать набор глобальных типов для Next.js; в тестах используются явные импорты из `vitest`.
