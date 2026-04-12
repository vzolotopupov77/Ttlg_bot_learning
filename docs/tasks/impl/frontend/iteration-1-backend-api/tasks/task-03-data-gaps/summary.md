# Задача 03 — Анализ пробелов схемы данных: summary

## Сделано

- В `docs/data-model.md` добавлены поля `users.password_hash`, `users.notes`, пять bool-флагов в `lessons`, таблицы `reschedule_requests` и `system_settings`, обновлены ER-диаграмма, физическая схема, индексы, строка G-03.
- ORM: `backend/src/ttlg_backend/storage/models.py` синхронизирован с документом.

## Отклонения

- PK `reschedule_requests` — UUID (как у остальных сущностей), не BIGINT, для согласованности с проектом.
