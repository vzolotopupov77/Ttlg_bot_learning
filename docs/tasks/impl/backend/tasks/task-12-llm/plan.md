# Задача 12: LLM-клиент и промпт — план

## Цель

Вызов OpenRouter через `openai.AsyncOpenAI` с `base_url` и ключом из `Settings`; сборка системного промпта с контекстом ученика.

## Файлы

- `llm/client.py` — `LLMClient`, таймаут `llm_timeout_seconds`, перевод ошибок провайдера в `LLMUnavailableError`
- `llm/prompt.py` — `build_system_prompt`, форматирование строк занятий/ДЗ
- `llm/errors.py` — исключение `LLMUnavailableError`
- `config.py` — `llm_timeout_seconds`, `OPENROUTER_*`, `LLM_MODEL`

## Тесты

- Dev-зависимость `respx`; `test_llm_client.py` — мок `POST .../chat/completions`, проверка отсутствия ключа в логах.
