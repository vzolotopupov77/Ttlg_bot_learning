# Задача 04: Физическая ER-диаграмма — итог

**Статус:** ✅ Done

---

## Что сделано

В [`docs/data-model.md`](../../../../../../data-model.md) добавлена секция **«Физическая схема»**, содержащая:

1. **PostgreSQL-типы всех колонок** для 6 таблиц (`users`, `lessons`, `assignments`, `progress`, `dialogues`, `messages`) в формате текстовых блоков с явным указанием NOT NULL / NULL и DEFAULT.

2. **Таблица FK-каскадов** — 7 внешних ключей с действиями `CASCADE` (6) и `SET NULL` (1).

3. **Таблица индексов** — 9 индексов, в том числе:
   - `users.telegram_id` UNIQUE
   - Простые B-tree индексы на все FK-колонки
   - `lessons.scheduled_at` (B-tree) — добавлен по результатам анализа сценария SC-S-01
   - `messages.(dialogue_id, created_at)` (composite B-tree) — добавлен по результатам анализа сценария SC-S-03

## Маппинг SQLAlchemy → PostgreSQL

| SQLAlchemy | PostgreSQL |
|-----------|-----------|
| `Uuid(as_uuid=True)` | `UUID` |
| `String(255)` | `VARCHAR(255)` |
| `String(512)` | `VARCHAR(512)` |
| `Text` | `TEXT` |
| `BigInteger()` | `BIGINT` |
| `Date` | `DATE` |
| `DateTime(timezone=True)` | `TIMESTAMPTZ` |
| `Integer` (mapped) | `INT` |
| `SQLEnum(..., native_enum=True)` | PostgreSQL enum type |

## Отклонений от плана нет
