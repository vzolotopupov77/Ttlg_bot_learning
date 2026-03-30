# Задача 13: Эндпоинт диалога — план

## Цель

Заменить stub `POST /v1/dialogue/message` на сценарий с БД и LLM по [api-contracts.md](../../../../tech/api-contracts.md).

## Логика

1. Найти `User` (роль `student`) по `telegram_id` → иначе `404 user_not_found`.
2. `dialogue_id`: проверка владения → иначе `404 dialogue_not_found`; иначе создать `Dialogue` (`channel=telegram`).
3. Сохранить сообщение пользователя → собрать контекст → вызвать LLM → сохранить ответ ассистента → `200` с полями контракта.
4. Ошибка LLM → `503 llm_unavailable`; откат транзакции при сбое после записи user message.

## Файлы

- `services/dialogue_service.py` — оркестрация
- `api/dialogue.py` — роутер, `Depends(get_llm_client)` для подмены в тестах
- Удалены: stub-хранилище, `DIALOGUE_STUB_ALLOWED_TELEGRAM_IDS`, `assistant_reply.py`

## Тесты

- SQLite в pytest: `TTLG_ALLOW_SQLITE_TEST=1`, сидирование пользователя через `POST /v1/users`.
- `test_dialogue_llm_error.py` — `503` при `LLMUnavailableError`.
