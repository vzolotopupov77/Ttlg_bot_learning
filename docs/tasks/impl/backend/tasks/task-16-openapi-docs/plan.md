# Задача 16: OpenAPI `/docs`, описания схем

**Статус:** завершена (см. [summary.md](summary.md)).

## Что меняется

- `backend/src/ttlg_backend/main.py` — `title`, `description`, `version` у `FastAPI`; `summary`/`description` у `GET /health`.
- `api/dialogue.py` — `summary`/`description` у `POST /dialogue/message`; модель ответа с `Field(description=...)` (или эквивалент в OpenAPI).
- `api/users.py`, `api/lessons.py`, `api/assignments.py` — `summary`/`description` у всех маршрутов; `Field(description=...)` у ключевых полей Pydantic-схем.
- Опционально: `Makefile` — цель `openapi-export` → `docs/openapi.json`.

## Файлы

- `backend/src/ttlg_backend/main.py`
- `backend/src/ttlg_backend/api/dialogue.py`
- `backend/src/ttlg_backend/api/users.py`
- `backend/src/ttlg_backend/api/lessons.py`
- `backend/src/ttlg_backend/api/assignments.py`
- при необходимости `Makefile`, `docs/openapi.json`
