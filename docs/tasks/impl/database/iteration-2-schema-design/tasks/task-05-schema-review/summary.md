# Задача 05: Ревью схемы через skill postgresql-table-design — итог

**Статус:** ✅ Done

---

## Что сделано

Применён чек-лист skill `postgresql-table-design`. Ниже — полная таблица решений по каждому пункту.

## Таблица решений

| # | Рекомендация / точка | Решение | Обоснование |
|---|---------------------|---------|------------|
| R-01 | `TIMESTAMPTZ` для всех timestamp-полей | ✅ Принято — подтверждено | Все datetime-поля используют `DateTime(timezone=True)` в ORM → `TIMESTAMPTZ` в PostgreSQL |
| R-02 | UUID PK (vs BIGINT IDENTITY) | ✅ Принято — оставить UUID | Система многокомпонентная (bot + backend + web); UUID обеспечивает глобальную уникальность и непрозрачность ID; решение зафиксировано в ADR-002 |
| R-03 | `UNIQUE(student_id, period_start, period_end)` на `progress` | ✅ Принято | Предотвращает дублирование агрегата за один период; добавлено в `data-model.md` как дополнительный constraint |
| R-04 | Composite index `(dialogue_id, created_at)` на `messages` | ✅ Принято | Покрывает сценарий SC-S-03: выборка сообщений диалога в порядке времени; добавлен в таблицу индексов |
| R-05 | Index на `lessons.scheduled_at` | ✅ Принято | Покрывает сценарий SC-S-01: `WHERE student_id = ? AND scheduled_at > now() ORDER BY scheduled_at LIMIT 1`; добавлен в таблицу индексов |
| R-06 | `Assignment.status = overdue` — механизм обновления | ✅ Зафиксировано | Обновляется вручную или фоновым процессом (задача приложения); зафиксировано в примечании к `Assignment` в `data-model.md` |
| R-07 | `updated_at` на `Lesson`, `Assignment` | ⏳ Отложено → задача 11 | Требует ORM-изменений и новой Alembic-ревизии; не блокирует MVP; добавить при необходимости аудита изменений |
| R-08 | NULL-семантика `Assignment.lesson_id` | ✅ Подтверждено | `SET NULL` корректна: ДЗ может существовать без привязки к занятию (выдано вне занятия) |
| R-09 | Именование enum-типов | ✅ Подтверждено | `user_role`, `lesson_status`, `assignment_status`, `dialogue_channel`, `message_role` — все в `snake_case`, соответствуют PostgreSQL-конвенции |
| R-10 | Нормализация `Progress` (денормализованный агрегат) | ✅ Принято (осознанно) | Денормализация явная и задокументированная; риск расхождения данных принят для MVP; автоматический пересчёт — будущая итерация |

## Пункты skill-чек-листа, не применимые к схеме

| Пункт | Обоснование неприменимости |
|-------|---------------------------|
| Partitioning | Таблицы MVP-размера (<100M rows); не актуально |
| Row-Level Security | Авторизация на уровне приложения (FastAPI); RLS — опционально при росте |
| JSONB | В текущей схеме нет полуструктурированных данных |
| Range types | Для `period_start`/`period_end` в `progress` range-тип избыточен |
| UNLOGGED/TEMP tables | Нет временных или ненадёжных таблиц |
| BRIN index | Нет таблиц с естественным порядком вставки и без случайных FK |

## VARCHAR vs TEXT (skill-рекомендация)

Skill рекомендует `TEXT` + `CHECK(LENGTH(col) <= n)` вместо `VARCHAR(n)`. Текущее решение — оставить `VARCHAR(255)` / `VARCHAR(512)`:

- ORM уже использует `String(255)` / `String(512)` — изменение потребует миграции
- Для документирования намерения «ограниченная длина» `VARCHAR` читаемее
- Риск: PostgreSQL выбросит ошибку при превышении, а не усечёт — поведение корректно

Если потребуется изменить — помечено для задачи 11 итерации 5.

## Изменения, внесённые в `docs/data-model.md`

1. Добавлен составной индекс `(dialogue_id, created_at)` на `messages`
2. Добавлен индекс `lessons.scheduled_at`
3. Добавлен constraint `UNIQUE(student_id, period_start, period_end)` на `progress`
4. Добавлено примечание о механизме обновления `Assignment.status = overdue`
5. Добавлено примечание о денормализации `Progress`

## Для задачи 11 итерации 5 (ORM-изменения)

- [ ] Добавить `updated_at` на `Lesson` и `Assignment` (если появится требование аудита)
- [ ] Добавить `Index("ix_messages_dialogue_created", "dialogue_id", "created_at")` в `models.py`
- [ ] Добавить `Index("ix_lessons_scheduled_at", "scheduled_at")` в `models.py`
- [ ] Добавить `UniqueConstraint("student_id", "period_start", "period_end")` на `Progress` в `models.py`
- [ ] Рассмотреть миграцию `VARCHAR` → `TEXT + CHECK` при необходимости
