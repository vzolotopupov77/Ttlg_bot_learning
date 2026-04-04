# Задача 06: Ревью и актуализация ADR-002

## Мета

| | |
|---|---|
| **Итерация** | 3 — Инструменты: документирование и практическая справка |
| **Статус** | 🚧 In Progress |
| **Дата** | 2026-04-04 |

## Цель

Проверить, что [`docs/adr/adr-002-orm-migrations-tests.md`](../../../../adr/adr-002-orm-migrations-tests.md) отражает фактически принятые решения. Зафиксировать то, что было решено в ходе реализации, но в ADR не попало.

## Анализ расхождений (установлено при планировании)

Сверка ADR-002 с кодом (`storage/models.py`, `backend/alembic/env.py`, `pyproject.toml`, `conftest.py`):

| Аспект | ADR-002 (было) | Реализация (факт) |
|--------|---------------|-------------------|
| UUID PK | не упомянут | `Uuid(as_uuid=True)` + `default=uuid.uuid4` во всех моделях |
| Enum-типы | не упомянут | `StrEnum` + `SQLEnum(native_enum=True, values_callable=...)` |
| asyncio_mode | не упомянут | `asyncio_mode = "auto"` + `asyncio_default_fixture_loop_scope = "function"` в корневом `pyproject.toml` |
| Текущая изоляция тестов | «задача 08 tasklist» | SQLite+aiosqlite (`TTLG_ALLOW_SQLITE_TEST=1`) — временное решение |
| Ссылка на PostgreSQL harness | «задача 08» | должно быть итерация 5, задача 13 |

## Затрагиваемые файлы

- `docs/adr/adr-002-orm-migrations-tests.md` — единственный изменяемый файл

## Состав изменений

### Секция «Решение» — добавить пункты 5–7

```
5. **UUID как тип первичного ключа** во всех таблицах: `Uuid(as_uuid=True)` + `default=uuid.uuid4`
   (не автоинкремент); генерация на стороне Python.
6. **StrEnum + native PostgreSQL enum**: `StrEnum` (Python 3.11+) + `SQLEnum(native_enum=True,
   values_callable=lambda e: [i.value for i in e])` — единый паттерн для всех enum-полей.
7. **pytest-asyncio**: `asyncio_mode = "auto"` + `asyncio_default_fixture_loop_scope = "function"`
   в корневом `pyproject.toml`; распространяется на backend-тесты через uv workspace.
```

### Секция «Последствия» — обновить пункт об изоляции

Заменить «задача 08 tasklist» на конкретное описание:
- Текущее состояние: SQLite+aiosqlite (`TTLG_ALLOW_SQLITE_TEST=1`) — принятое временное решение; позволяет запускать тесты без поднятого PostgreSQL.
- PostgreSQL test harness реализуется в **итерации 5 (задача 13)**: транзакционная изоляция или тестовая база; `TTLG_ALLOW_SQLITE_TEST` снимается.

### Дата ADR

Обновить с `2026-03-29` на `2026-04-04`.

## Definition of Done

- ADR содержит явные пункты: UUID PK, StrEnum+native_enum, asyncio_mode
- Ссылка на harness указывает на итерацию 5 / задачу 13
- SQLite-изоляция описана как временное решение с явным сроком замены
- Дата ADR обновлена
- Разделы «Контекст» и «Рассмотренные варианты» — не тронуты
