# Участие в разработке

## Ветки

- Рабочие ветки с префиксом задачи/темы (например `feat/…`, `fix/…`) — по договорённости команды.
- Базовая ветка по умолчанию — `main` или та, которую укажет maintainer.

## Локальная проверка перед PR

```bash
make check
```

Состав: **`make lint`** (Ruff) + **`make backend-test`** (PostgreSQL `ttlg_test`) + **`make bot-test`** + **`make frontend-lint`**.  
**`make frontend-test`** (Vitest) в `check` **не** входит — запускайте отдельно при изменениях фронта.

См. также [onboarding.md](onboarding.md#3-проверка-что-всё-работает).

## Что коммитить

- **Да:** исходники, тесты, миграции, обновлённую документацию по факту изменений, при смене API — [openapi.json](openapi.json) (`make openapi-export`).
- **Нет:** `.env` с реальными секретами, локальные артефакты сборки, случайно сгенерированные `node_modules/`, `.venv/` (они в ignore).

## Кодстайл

- Python: Ruff (линт + формат), соглашения — [.cursor/rules/conventions.mdc](../.cursor/rules/conventions.mdc).
- Фронт: ESLint/Prettier по конфигу `frontend/`.

## Согласование крупных изменений

Принцип «план → согласие → реализация → summary» — [.cursor/rules/workflow.mdc](../.cursor/rules/workflow.mdc) и [plan.md](plan.md).
