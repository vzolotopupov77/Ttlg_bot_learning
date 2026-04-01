# Задача 19: линт и формат — summary

**Статус:** ✅ завершена.

## Сделано

- В корневом `pyproject.toml` добавлена dev-зависимость **ruff** (`[dependency-groups] dev`), секции `[tool.ruff]` / `[tool.ruff.lint]` (target py312, line-length 120, правила E/F/I/UP/B/SIM; для `backend/alembic/**/*.py` отключены E501 и E402).
- `Makefile`: цели `lint`, `format`, `check` (lint + `backend-test` + `bot-test`).
- `README.md`: блок «Тесты и линт» с перечислением команд.
- `.cursor/rules/conventions.mdc`: упоминание `make lint` / `make check`.
- Прогон `ruff format` и правки по замечаниям (в т.ч. `StrEnum` в ORM, list comprehension в `dialogue_service`, `contextlib.suppress` в боте).

## Отклонения

- Длинные строки в Alembic не форсились: игнор E501 только для `backend/alembic/**/*.py`.

## Проверка

- `make check` — успешно.
