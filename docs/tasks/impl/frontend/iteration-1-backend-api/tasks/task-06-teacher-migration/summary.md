# Задача 06 — Миграция преподавателя: summary

## Сделано

- Файл `backend/alembic/versions/c9d0e1f2a3b4_seed_teacher_vladimir.py`: пользователь `Владимир`, email `vzolotoy@mail.ru`, `password_hash` через `bcrypt.hashpw`; пароль из `TEACHER_DEFAULT_PASSWORD` или дефолт `changeme_teacher`.
- `.env.example` дополнен `TEACHER_DEFAULT_PASSWORD`.

## Проверка

- После миграций: `POST /v1/auth/login` с email `vzolotoy@mail.ru`, паролем из env, `role`: `teacher` → 200 и cookie с JWT.
