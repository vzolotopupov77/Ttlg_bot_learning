# Задача 08: Summary

## Сделано

- [backend/pyproject.toml](../../../../../../backend/pyproject.toml): `[project.optional-dependencies] dev` — `pytest`, `pytest-asyncio`, `httpx`.
- [pyproject.toml](../../../../../../pyproject.toml) (корень): `[tool.pytest.ini_options]` — `asyncio_mode=auto`, `asyncio_default_fixture_loop_scope=function`; настройки единые для всего workspace.
- [Makefile](../../../../../../Makefile): цель `backend-test` — `uv run --package ttlg-backend --extra dev pytest backend/tests -v`.
- [backend/tests/\_\_init\_\_.py](../../../../../../backend/tests/__init__.py): добавлен маркер пакета.
- [backend/tests/conftest.py](../../../../../../backend/tests/conftest.py):
  - autouse-фикстуры `reset_cached_settings` и `reset_stub_dialogue` с типами `Generator[None, None, None]` — изоляция состояния между тестами.
  - Общая фикстура `dialogue_client` (async, typed `AsyncGenerator[AsyncClient, None]`) — единый источник HTTP-клиента + mock LLM для всех тестов диалога.
- [backend/tests/test_health.py](../../../../../../backend/tests/test_health.py): smoke `GET /health` без `DATABASE_URL` → **503** `degraded`/`not_configured`; без избыточных декораторов `@pytest.mark.asyncio`.

## Проверка

- `make backend-test` — exit 0, **8 passed**.
