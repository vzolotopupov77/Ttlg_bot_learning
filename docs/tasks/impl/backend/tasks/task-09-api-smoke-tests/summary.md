# Задача 09: Summary

## Сделано

- [backend/src/ttlg_backend/main.py](../../../../../../backend/src/ttlg_backend/main.py): обработчик `RequestValidationError` → единый формат `{"error": {"code": "validation_error", …}}`; роутер диалога подключён с префиксом `/v1`.
- [backend/src/ttlg_backend/api/dialogue.py](../../../../../../backend/src/ttlg_backend/api/dialogue.py): stub `POST /v1/dialogue/message` — in-memory хранилище диалогов, allowlist `DIALOGUE_STUB_ALLOWED_TELEGRAM_IDS`, field-validator на непустой `text`.
- [backend/src/ttlg_backend/services/assistant_reply.py](../../../../../../backend/src/ttlg_backend/services/assistant_reply.py): `default_assistant_reply` — stub-заглушка; в тестах заменяется через `app.dependency_overrides[get_assistant_reply]`.
- [backend/tests/test_dialogue.py](../../../../../../backend/tests/test_dialogue.py): 7 тестов:
  - `test_dialogue_success` — 200, все поля контракта.
  - `test_dialogue_continue_with_dialogue_id` — второй запрос с `dialogue_id` сохраняет тот же id.
  - `test_dialogue_empty_text_returns_422` — whitespace-only text.
  - `test_dialogue_unknown_user_returns_404` — `user_not_found`.
  - `test_dialogue_missing_required_fields[missing_telegram_id|missing_text|empty_body]` — параметризованные 422.
- [.env.example](../../../../../../.env.example): закомментированная подсказка по `DIALOGUE_STUB_ALLOWED_TELEGRAM_IDS`.

## Mock LLM

Фикстура `dialogue_client` в [conftest.py](../../../../../../backend/tests/conftest.py) устанавливает `app.dependency_overrides[get_assistant_reply] = lambda: mock_reply` и сбрасывает после теста. Реальный OpenRouter не вызывается.

## Отклонения от исходного плана

Тесты написаны не как `xfail`, а как **проходящие** — stub-реализация роутера добавлена в той же итерации (задача 09), чтобы `make backend-test` был зелёным. При реализации задачи 13 stub заменяется на полноценный сервис без изменения URL-контракта.

## Проверка

- `make backend-test` — **8 passed**, exit 0.
