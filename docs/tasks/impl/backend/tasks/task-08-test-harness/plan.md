# Задача 08: Pytest + окружение, фикстуры, `make backend-test`

## Цель

Подключить dev-зависимости **pytest**, **pytest-asyncio**, **httpx**; настроить вызов ASGI-приложения через `httpx.AsyncClient` + `ASGITransport` ([ADR-002](../../../../../adr/adr-002-orm-migrations-tests.md)); добавить цель **make backend-test**; первый smoke-тест на `GET /health` с управляемым `DATABASE_URL` через env в тестах.

## Что меняется

- [backend/pyproject.toml](../../../../../../backend/pyproject.toml): секция `[project.optional-dependencies]` с группой `dev` (`pytest`, `pytest-asyncio`, `httpx`); при необходимости синхронизация с корневым workspace uv.
- [backend/tests/conftest.py](../../../../../../backend/tests/conftest.py): фикстура async-клиента, сброс/подмена env (`DATABASE_URL` и др.) через `monkeypatch` или `autouse`, чтобы тесты не требовали живой БД на этапе без ORM.
- [backend/tests/test_health.py](../../../../../../backend/tests/test_health.py): минимум один тест `/health` с явным ожидаемым кодом (например **503** при отсутствии `DATABASE_URL`, как в прод-коде).
- [Makefile](../../../../../../Makefile): цель `backend-test` (например `uv run --package ttlg-backend pytest backend/tests -v` с рабочей директорией из корня репо).
- [.PHONY](../../../../../../Makefile): дополнить `backend-test`.

## Изоляция БД на этапе 8

ORM и миграции — задача 10. Достаточно:

- в тестах задать `DATABASE_URL` пустым/отсутствующим там, где проверяется деградация health;
- при необходимости отдельный кейс с тестовым URL и поднятой БД — опционально, не блокер DoD задачи 08.

Конкретика фикстур фиксируется здесь без противоречия ADR-002 (транзакции/отдельная БД — усиление после появления `AsyncSession` в тестах).

## Ориентир фикстуры клиента

```python
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
```

Импорт `app` — из `ttlg_backend.main`.

## Definition of Done

- `make backend-test` завершается с кодом **0**.
- Нет `ImportError` при сборке тестов.
- В CI (если появится) используется та же команда, что в Makefile.
- Документ итерации: [iteration-4-tests/plan.md](../../iteration-4-tests/plan.md).

## Документы

- Summary: [summary.md](summary.md)
