# Задача 04 — Новые endpoints backend: summary

## Сделано

- Конфиг: `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES` (обязательные правила валидации).
- Роутеры: `api/auth.py`, `api/deps.py`, `api/teacher.py`, `api/students.py`, `api/settings.py`, `api/student_schedule.py`; расширен `api/lessons.py`.
- Репозитории: `teacher_repo`, `settings_repo`, расширены `users`, `lessons`, `dialogues`.
- Сервис: `services/auth_service.py` (JWT + bcrypt).
- `main.py`: регистрация роутеров, обработчик `HTTPException`.
- Зависимости: `python-jose[cryptography]`, `bcrypt`.
- Тесты: `backend/tests/test_auth_and_teacher.py`.

## Отклонения

- Старые MVP-роуты (`POST /v1/users`, `POST /v1/lessons` без JWT) оставлены с `require_auth` (заглушка) для совместимости с существующими тестами; новые мутации занятий требуют JWT.
