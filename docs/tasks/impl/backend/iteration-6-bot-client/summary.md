# Итерация 6 (рефакторинг бота) — summary

**Статус:** ✅ Done

## Результат

- Бот переведён на вызов backend API; прямой LLM из процесса бота удалён.
- Документация: README (smoke), Makefile, vision, tasklist.

## Задачи


| Задача | Summary                                                                                        |
| ------ | ---------------------------------------------------------------------------------------------- |
| 14     | [../tasks/task-14-bot-client/summary.md](../tasks/task-14-bot-client/summary.md)               |
| 15     | [../tasks/task-15-integration-smoke/summary.md](../tasks/task-15-integration-smoke/summary.md) |


## Регрессия

- `make backend-test` — 16 passed.

## Самопроверка (этап 6)

### Автоматическая (зафиксировано при закрытии итерации)


| Проверка                                                                                                  | Результат    |
| --------------------------------------------------------------------------------------------------------- | ------------ |
| В `src/ttlg_bot/services/` есть `backend_client.py`, `chat_service.py`; нет `llm_client.py`, `history.py` | OK           |
| В `src/` нет вхождений `openai` / `AsyncOpenAI` (`rg`)                                                    | OK           |
| Корневой `pyproject.toml`: в `dependencies` нет `openai`, есть `httpx`                                    | OK           |
| `.env.example` содержит `BACKEND_URL`, `BACKEND_TIMEOUT`                                                  | OK           |
| `Settings` содержит `backend_url`, `backend_timeout`                                                      | OK           |
| `uv run python -c "import ttlg_bot"`                                                                      | OK           |
| `make backend-test`                                                                                       | 16 passed    |
| `make bot-test`                                                                                           | 7 passed     |
| Цели Makefile: `install`, `run`, `bot-test`, `smoke-integration`, `backend-`*                             | присутствуют |


### Интеграционные тесты `make bot-test` (зафиксировано)

Паттерн: `httpx.AsyncClient(transport=ASGITransport(app=app))` — `BackendClient` против реального FastAPI-приложения (SQLite in-memory, mock LLM).


| Тест                                                       | Сценарий                                                    |
| ---------------------------------------------------------- | ----------------------------------------------------------- |
| `test_send_message_success`                                | Известный пользователь → ответ-строка                       |
| `test_dialogue_id_persisted_across_messages`               | 2-е сообщение содержит `dialogue_id` из первого ответа      |
| `test_unknown_user_raises_backend_error_with_user_message` | 404 `user_not_found` → `BackendError` с текстом про профиль |
| `test_empty_text_raises_backend_error`                     | 422 (пустой текст) → `BackendError`                         |
| `test_llm_unavailable_returns_friendly_message`            | 503 `llm_unavailable` → текст про ассистента                |
| `test_invalid_dialogue_id_cleared_on_not_found`            | 404 `dialogue_not_found` → кэш `dialogue_id` сброшен        |
| `test_connect_error_raises_service_down`                   | `ConnectError` → `BackendError` "сервис недоступен"         |


Попутно исправлен `test_health_without_database_returns_503` в `backend/tests/`: `delenv` заменён на `setenv("DATABASE_URL", "")` — env var перекрывает `.env`-файл при повторной инициализации `Settings`.

### Ручная (по чеклисту README / задач 14–15)

- [x] Без `BACKEND_URL` в конфиге — ошибка валидации Pydantic (`backend_url` field required), не `KeyError` *(лог 17:44)*.
- [x] Backend не запущен, `BACKEND_URL` задан — в Telegram fallback «Сервис временно недоступен…» через `ConnectError`, без traceback *(лог 17:46)*.
- [x] Пользователь без `POST /v1/users` — бот показал fallback (500 → `internal_error`), не упал *(лог 18:13; до исправления конфига БД)*.
- [x] Полный smoke end-to-end *(2026-03-31 20:17)*:
  - SQLite (`DATABASE_URL=sqlite+aiosqlite:///./local.db`, `TTLG_ALLOW_SQLITE_TEST=1`)
  - `make backend-run` → `GET /health` → 200 OK
  - `POST /v1/users` (реальный `telegram_id`) → 201 Created
  - `make run` (timeout=90s) → сообщение в Telegram → `POST /v1/dialogue/message` 200 OK
  - LLM-ответ от `openai/gpt-4o-mini` через OpenRouter получен (~40 сек с retry)
  - Ответ доставлен в Telegram ✓

**Найдено в процессе smoke:** `BACKEND_TIMEOUT=30` недостаточно при LLM retry (>30 сек). Исправлено: `BACKEND_TIMEOUT=90` в `.env.example` (рекомендация).

