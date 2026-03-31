# Задача 16: OpenAPI `/docs` — summary

**Статус:** завершена.

## Сделано

- `main.py`: `TTLG Backend`, описание, `version=0.1.0`; `GET /health` — тег `health`, `summary`/`description`.
- `dialogue.py`: `DialogueMessageResponse` + `response_model`; русскоязычные описания запроса/операции.
- `users.py`, `lessons.py`, `assignments.py`: `summary`/`description` у CRUD; поля схем с `Field(description=...)`.
- `Makefile`: цель `openapi-export` → `docs/openapi.json`.

## Ручная проверка

- `/docs` открыт при локальном запуске (сценарий SQLite).

## Отклонения

- Нет.
