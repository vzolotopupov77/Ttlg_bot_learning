# Задача 05 — Миграция с mock-данными: summary

## Сделано

- Файл `backend/alembic/versions/b8c9d0e1f2a3_seed_mock_data.py`: преподаватель-заглушка, 4 ученика, 12 занятий, `system_settings`, диалог с 6 сообщениями, один `reschedule_requests`.

## Примечания

- `downgrade()` удаляет вставленные строки по фиксированным UUID.
