# Задача 09: Smoke API-тесты сценария сообщений (контракт диалога)

## Цель

Покрыть HTTP-сценарии **как у тонкого клиента (бот)**: `POST /v1/dialogue/message` по [api-contracts.md](../../../../../tech/api-contracts.md) и формату ошибок [api-conventions.md](../../../../../api-conventions.md); **без** реального вызова LLM (mock); негативы: валидация, неизвестный пользователь.

## Что меняется

- [backend/tests/test_dialogue.py](../../../../../../backend/tests/test_dialogue.py): тесты на JSON-тело и коды ответа.
- При необходимости доработка `backend/tests/conftest.py` — общие фикстуры, переопределения зависимостей FastAPI.

## Сценарии (минимум)

| Кейс | Ожидание |
|------|----------|
| Валидный `telegram_id` + непустой `text` | **200**, тело с `dialogue_id`, `message_id`, `text`, `created_at` (LLM замокан) |
| Пустой / невалидный `text` | **422**, `error.code` в духе `validation_error` |
| Неизвестный `telegram_id` | **404**, `user_not_found` |

Запросы — те же, что отправит бот: `Content-Type: application/json`, при необходимости заголовок `X-User-Role` (см. контракт).

## Mock LLM

- Через **dependency_overrides** в FastAPI: подмена зависимости, отвечающей за вызов провайдера, фиктивным ответом.
- Секреты и ключи OpenRouter в smoke **не** хардкодить; opt-in integration с реальным ключом — отдельная маркировка (`pytest.mark.integration`), вне обязательного `make backend-test`.

## Связь с реализацией эндпоинта

Роут `POST /v1/dialogue/message` вводится в **задаче 13**. До этого момента тесты могут:

- помечаться `@pytest.mark.xfail(reason="…")`, или
- быть заскипованы условно, пока роутер не смонтирован,

при условии, что **после задачи 13** все сценарии проходят без xfail (см. DoD задачи 13 в tasklist).

Предпочтительно: с первого прохода писать финальные asserts; падение набора до задачи 13 ожидаемо в коротком окне — зафиксировать в summary задачи 09.

## Definition of Done

- Минимум **два** теста в смысле полярностей: успешный ответ (с mock) и ошибка клиента (422 или 404).
- `pytest` собирает модуль без ошибок импорта.
- Нет секретов в коде тестов.

## Документы

- Summary: [summary.md](summary.md)
- Итерация: [iteration-4-tests/plan.md](../../iteration-4-tests/plan.md)
