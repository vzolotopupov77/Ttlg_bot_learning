# Задача 14: бот как тонкий клиент — summary

**Статус:** ✅ Done

## Сделано

- Добавлен `src/ttlg_bot/services/backend_client.py` (`httpx`, `POST /v1/dialogue/message`, кэш `dialogue_id` по `telegram_id`, маппинг ошибок в короткие тексты).
- `config.py`: `backend_url` (`HttpUrl`), `backend_timeout`; удалены поля OpenRouter/LLM из настроек бота.
- `chat_service.py` использует только `BackendClient`; удалены `llm_client.py`, `history.py`.
- `__main__.py`: инициализация `BackendClient`, `aclose()` в `finally` после polling.
- Корневой `pyproject.toml`: зависимость `httpx`, удалён `openai` из пакета бота.
- `.env.example`: `BACKEND_URL`, `BACKEND_TIMEOUT`; переменные LLM помечены как для backend.
- [docs/vision.md](../../../../vision.md): актуальная структура `src/ttlg_bot/`, переменные окружения бота.

## Проверки

- В `src/` нет вхождений `openai`.
- `make backend-test` — 16 passed.

## Отклонения

- Нет.
