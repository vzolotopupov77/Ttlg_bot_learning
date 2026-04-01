# Задача 19: линт и формат (Ruff)

**Статус:** завершена (см. [summary.md](summary.md)).

## Что меняется

- Зависимость **ruff** в workspace (корневой `pyproject.toml`).
- Секция `[tool.ruff]` с охватом `src/`, `backend/src/`, `tests/`, `backend/tests/`.
- **Makefile:** `lint`, `format`, `check` (линт + `backend-test` + `bot-test`).
- **README:** строка про проверки перед PR.
- При необходимости — фраза в `.cursor/rules/conventions.mdc` про `make lint` / `make format`.

## Definition of Done

- `make lint` и `make format` завершаются без ошибок на дереве репозитория.
- Игноры Ruff — точечные и задокументированы в конфиге.
