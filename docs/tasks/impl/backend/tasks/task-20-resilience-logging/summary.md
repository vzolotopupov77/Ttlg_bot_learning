# Задача 20: устойчивость и логи — summary

**Статус:** ✅ завершена.

## Сделано

- **Инвентаризация HTTP:** `LLMClient` (AsyncOpenAI + `llm_timeout_seconds`), `BackendClient` (httpx).
- **Бот:** для встроенного `httpx.AsyncClient` задан `httpx.Timeout(total, connect=min(10, total))` — отдельный лимит на установку соединения.
- **Fallback:** без изменений цепочки: LLM → `LLMUnavailableError` → HTTP 503 `llm_unavailable` → в Telegram `MSG_LLM_UNAVAILABLE` (уже покрыто интеграционными тестами).
- **Логи:** добавлен тест `backend/tests/test_llm_client.py` — `test_llm_client_api_error_does_not_log_secret_key` (ответ 401, в логах нет ключа и `Authorization`).
- **`docs/vision.md`:** уточнение про обобщённые сообщения при сбоях LLM и неверном ключе, без утечки секретов.

## Примечание для пользователя

- Неверный `OPENROUTER_API_KEY` с точки зрения ученика в Telegram даёт то же обобщённое сообщение, что и временная недоступность ассистента; исправление — настройка `.env` администратором.

## Проверка

- `make check` — успешно.
