# Итерация 8 (Backend Tasklist): качество и инженерные практики — summary

**Статус:** ✅ завершена. План: [plan.md](plan.md).

## Результат

- Единый **Ruff** для `src/`, `backend/src/`, тестов и Alembic; команды `make lint`, `make format`, `make check`.
- Уточнены **таймауты httpx** в боте (connect отдельно от read); цепочка **fallback при сбое LLM** подтверждена тестами.
- Усилена проверка **логов** при ошибке API провайдера; в **vision** зафиксировано требование не раскрывать секреты пользователю и в логах.
- Dev-зависимости (pytest, httpx, aiosqlite, respx, ruff) переведены из `[project.optional-dependencies]` в **`[dependency-groups] dev`** (PEP 735); добавлен `[tool.uv] default-groups = ["dev"]` — одна команда `uv sync` / `make install` даёт рабочую среду.
- Зафиксирован **[ADR-003](../../../../adr/adr-003-quality-tooling.md)**: Ruff, dependency-groups, отложенный тайпчекер (кандидат ty). Обновлён `docs/adr/README.md` и `.cursor/rules/conventions.mdc`.
- В [tasklist-backend.md](../../../tasklist-backend.md) обновлены статусы задач 19–20 и блок **«Проверка этапа 8 (самопроверка)»**.

## Задачи

| № | Summary |
|---|---------|
| 19 | [tasks/task-19-lint-format/summary.md](tasks/task-19-lint-format/summary.md) |
| 20 | [tasks/task-20-resilience-logging/summary.md](tasks/task-20-resilience-logging/summary.md) |

## Самопроверка (агент)

- `make check` — выполнено: lint + 17 backend tests + 7 bot tests.
- `uv sync` после удаления venv — dev-группа ставится автоматически.
