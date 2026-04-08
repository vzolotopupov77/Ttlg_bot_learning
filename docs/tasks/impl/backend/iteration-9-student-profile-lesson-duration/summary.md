# Итерация 9: summary

**Статус:** завершена

## Сделано

- В `users`: `class_label`, `phone`, `email` (NULL); в `lessons`: `duration_minutes` NOT NULL DEFAULT 60, CHECK `> 0`.
- Миграция `a3f8c91d2b04_user_profile_lesson_duration`; Pydantic-схемы `UserCreate`/`UserRead`, `LessonCreate`/`LessonRead`; репозитории обновлены.
- Зависимость `email-validator` в `backend/pyproject.toml`.
- Документы: `data-model.md`, `api-contracts.md`, `integrations.md`, `user-scenarios.md`, `vision.md`.
- Smoke-тесты: дефолт и кастомная длительность урока, создание пользователя с профилем.

## Отклонения

- Уникальность `email` не вводилась (MVP); при необходимости — отдельная задача + `409 conflict`.

## Проверка

- `uv run ruff check` на изменённых модулях; полный `backend-test` — при доступной БД `DATABASE_TEST_URL` (`make backend-db-test-create` при необходимости).
