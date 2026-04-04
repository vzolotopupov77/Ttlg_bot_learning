# Задача 07: Практическая справка `docs/tech/db-guide.md`

## Мета

| | |
|---|---|
| **Итерация** | 3 — Инструменты: документирование и практическая справка |
| **Статус** | 🚧 In Progress |
| **Дата** | 2026-04-04 |

## Цель

Создать `docs/tech/db-guide.md` — практическую справку по работе с БД в проекте для агентов и разработчиков. Документ не дублирует ADR, а объясняет «как делать» на практике.

## Затрагиваемые файлы

- `docs/tech/db-guide.md` — новый файл (единственный артефакт)

## Структура документа

### Раздел 1: Структура слоя данных

Описание файлов и их ответственности:

| Файл | Ответственность |
|------|----------------|
| `backend/src/ttlg_backend/storage/models.py` | ORM-модели и StrEnum-перечисления |
| `backend/src/ttlg_backend/storage/repositories/` | 5 репозиториев: users, lessons, assignments, dialogues, progress_summary |
| `backend/src/ttlg_backend/db.py` | движок, фабрика сессий, `get_session`, `init_db`, `ping_db` |
| `backend/src/ttlg_backend/dependencies.py` | FastAPI-зависимости (auth placeholder) |
| `backend/alembic/` | конфиг и ревизии Alembic |

### Раздел 2: Миграции

**Существующие make-цели (Makefile):**
- `make backend-db-up` — `docker compose up -d db`
- `make backend-db-migrate` — `alembic -c backend/alembic.ini upgrade head`

**Прямые команды (через uv run):**
```bash
# создать новую ревизию
uv run --package ttlg-backend alembic -c backend/alembic.ini revision --autogenerate -m "description"

# проверить сгенерированный файл
# backend/alembic/versions/<rev>_description.py

# применить
uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

# откатить на 1 шаг
uv run --package ttlg-backend alembic -c backend/alembic.ini downgrade -1

# посмотреть текущую версию
uv run --package ttlg-backend alembic -c backend/alembic.ini current

# история ревизий
uv run --package ttlg-backend alembic -c backend/alembic.ini history --verbose
```

**Примечание:** `backend-db-shell`, `backend-db-reset` будут добавлены в итерации 4 (задача 08).

### Раздел 3: Репозитории

**Паттерн** (на основе существующих файлов в `storage/repositories/`):
- Каждый репозиторий — отдельный класс, принимает `AsyncSession` в `__init__`
- Методы: `get_by_id` → `session.get(Model, id)`, `list` → `select`, `create` → `session.add + commit`
- `None` при `get_by_id` возвращается явно (не исключение на уровне репозитория)

**Типовой шаблон нового репозитория** — кодовый блок с `import uuid`, классом, тремя методами.

### Раздел 4: Сессия в FastAPI

- `get_session` из `db.py` — async generator, оборачивает `async_sessionmaker`
- Инжекция через `Depends(get_session)` в endpoint
- Rollback при исключении — автоматический (в `get_session`)
- Репозиторий создаётся внутри endpoint, принимает сессию

### Раздел 5: SQL-сниппеты (5 штук)

Для использования через `make backend-db-shell` (итерация 4) или `psql` напрямую:

1. Все пользователи с ролями
2. Занятия конкретного ученика (JOIN users на teacher, статус)
3. ДЗ с истёкшим дедлайном
4. Последние 10 сообщений в диалогах
5. Прогресс по всем ученикам

**Примечание:** проверка сниппетов на seed-данных — задача 10, итерация 4.

## Definition of Done

- Файл `docs/tech/db-guide.md` создан
- Содержит 4 раздела (структура, миграции, репозитории, сессия)
- Все make-цели, упомянутые в разделе «Миграции», существуют в Makefile или явно помечены как «итерация 4»
- 5 SQL-сниппетов синтаксически корректны для PostgreSQL и схемы из `data-model.md`
- Нет ссылок на несуществующие файлы
