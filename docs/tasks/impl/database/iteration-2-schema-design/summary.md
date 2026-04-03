# Итерация 2: Проектирование схемы данных — итог

**Статус:** ✅ Done

---

## Что сделано

Полностью обновлён [`docs/data-model.md`](../../../../data-model.md) — теперь это актуальный единый источник правды по схеме. Документ содержит:

1. **Обновлённую логическую модель** (задача 03): все 6 сущностей с корректными типами, nullable, FK-каскадами и значениями по умолчанию — синхронизировано с `storage/models.py`.

2. **Физическую ER-диаграмму** (задача 04): PostgreSQL-типы всех колонок, таблица FK-каскадов, таблица индексов.

3. **Результаты ревью схемы** (задача 05): 10 точек проверки по skill `postgresql-table-design` — все отработаны явно; 3 рекомендации приняты и внесены в документ.

## Ключевые изменения `docs/data-model.md`

| Тип изменения | Детали |
|---------------|--------|
| PK всех сущностей | `UUID / int` → `UUID` |
| `User.telegram_id` | `int (nullable)` → `BIGINT (nullable, UNIQUE)` |
| Timestamps | `datetime` → `TIMESTAMPTZ` |
| Строковые поля | добавлены `VARCHAR(255)` / `VARCHAR(512)` |
| FK-каскады | задокументированы для всех 7 FK |
| Индекс `lessons.scheduled_at` | добавлен (SC-S-01) |
| Индекс `messages.(dialogue_id, created_at)` | добавлен composite (SC-S-03) |
| Constraint `UNIQUE(student_id, period_start, period_end)` | добавлен на `progress` |
| Пробелы G-01…G-05 | все явно закрыты: 2 отложены, 1 отложен, 1 зафиксирован, 1 подтверждён |

## Решения по пробелам итерации 1

| G | Решение |
|---|---------|
| G-01 Topic | Отложено — MVP покрыт `Lesson.topic VARCHAR(512)` |
| G-02 Material | Отложено — зависит от G-01 |
| G-03 Reschedule | Отложено — не блокирует MVP |
| G-04 Progress пересчёт | Зафиксировано: вручную через API |
| G-05 Lesson.notes | Подтверждено как достаточное |

## Для задачи 11 итерации 5

Четыре ORM-изменения помечены как отложенные (не внесены в `models.py`):
- Composite index на `messages(dialogue_id, created_at)`
- Index на `lessons.scheduled_at`
- UniqueConstraint на `progress(student_id, period_start, period_end)`
- Опционально: `updated_at` на `Lesson` и `Assignment`

## Отклонений от плана нет
