# Задача 14: бот как тонкий клиент backend

**Статус:** завершена (см. [summary.md](summary.md))

## Что меняется

- `src/ttlg_bot/config.py` — `backend_url`, `backend_timeout`; удалены поля OpenRouter/LLM для бота.
- Новый `src/ttlg_bot/services/backend_client.py` — `httpx.AsyncClient`, маппинг ошибок, кэш `dialogue_id` по `telegram_id`.
- `src/ttlg_bot/services/chat_service.py` — только `BackendClient`.
- `src/ttlg_bot/__main__.py` — инициализация `BackendClient`, `aclose` при остановке.
- Удалены `llm_client.py`, `history.py`.
- Корневой `pyproject.toml` — `httpx` в основных зависимостях, `openai` убран.
- `.env.example` — `BACKEND_URL`; переменные LLM помечены как для backend.

## Файлы

- См. список в сводном плане итерации 6 в тасклисте.
