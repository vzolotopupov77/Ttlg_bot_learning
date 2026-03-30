# Задача 13: Эндпоинт диалога — summary

**Статус:** завершена

## Итог

- Диалог персистентный: `dialogues` + `messages` (user + assistant).
- Контекст LLM: последние занятия и ДЗ ученика из репозиториев.
- Тесты задачи 09 (`test_dialogue.py`) проходят на SQLite с моком `get_llm_client`.
- Дополнительно: `test_dialogue_llm_error.py` для `503 llm_unavailable`.

## Тестовая БД

- Для CI/локально без Docker: в тестах используется `sqlite+aiosqlite:///:memory:` при `TTLG_ALLOW_SQLITE_TEST=1` (см. `conftest.py`, `ensure_sqlite_schema`).
- Продакшен/интеграция: PostgreSQL + `make backend-db-migrate`.
