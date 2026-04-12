# Итерация 1 — Реализация API для frontend: план

## Цель

Реализовать в backend все endpoints, спроектированные в Итерации 0; расширить схему данных (флаги занятий, запросы на перенос, настройки системы, аутентификация); наполнить БД mock-данными; добавить преподавателя в БД.

## Ценность

После завершения итерации backend полностью покрывает потребности 5 экранов frontend: разработка Итерации 2 (каркас) и последующих экранов может вестись с реальным API без заглушек.

## Входные данные

| Документ | Роль |
|----------|------|
| [docs/tech/api-contracts.md](../../../tech/api-contracts.md) | Контракты всех endpoints для frontend |
| [docs/data-model.md](../../../data-model.md) | Текущая схема БД (6 таблиц) |
| [docs/spec/frontend-requirements.md](../../../spec/frontend-requirements.md) | Требования к 5 экранам |
| [docs/api-conventions.md](../../../api-conventions.md) | Единый формат ошибок, пагинация |

## Состав задач

| № | Задача | Зависимость | Документы |
|---|--------|-------------|-----------|
| 03 | Анализ пробелов схемы данных | — | [план](tasks/task-03-data-gaps/plan.md) |
| 04 | Новые endpoints backend | после 03 | [план](tasks/task-04-new-endpoints/plan.md) |
| 05 | Миграция с mock-данными | после 04 (DDL) | [план](tasks/task-05-mock-migration/plan.md) |
| 06 | Миграция: добавить преподавателя | после 04 (DDL) | [план](tasks/task-06-teacher-migration/plan.md) |

## Пробелы схемы (сводка)

Отсутствующие поля и таблицы относительно API-контрактов Итерации 0:

- `users.password_hash TEXT NULL` — аутентификация
- `users.notes TEXT NULL` — заметки/цели ученика (поле в CRUD-форме)
- `lessons`: 5 bool-флагов `BOOLEAN NOT NULL DEFAULT false`:
  `notification_sent`, `confirmed_by_student`, `homework_sent`, `solution_received`, `solution_checked`
- Новая таблица `reschedule_requests` (FK на `lessons` + `users`, статус `TEXT CHECK`)
- Новая таблица `system_settings` (`key TEXT PRIMARY KEY`, `value TEXT NOT NULL`)

## Новые компоненты backend

### Роутеры (добавляемые файлы)

| Файл | Endpoints |
|------|-----------|
| `api/auth.py` | POST /v1/auth/login, POST /v1/auth/logout, GET /v1/auth/me |
| `api/teacher.py` | GET schedule, bot-requests, unconfirmed, pending-hw; POST remind-*; GET/PATCH reschedule-requests |
| `api/students.py` | CRUD /v1/students + /{id}/lessons, /{id}/dialogue, /{id}/stats |
| `api/settings.py` | GET/PUT /v1/settings |
| `api/deps.py` | `get_current_user` — JWT decode с `algorithms=["HS256"]` |
| `api/lessons.py` | Расширить: PUT, DELETE, PATCH /flags |

### Сервисы и репозитории (добавляемые файлы)

| Файл | Назначение |
|------|-----------|
| `services/auth_service.py` | bcrypt verify/hash, JWT encode/decode |
| `services/teacher_service.py` | Запросы дашборда, агрегаты |
| `services/students_service.py` | CRUD учеников, история занятий |
| `services/settings_service.py` | Чтение/запись key-value |
| `storage/repositories/teacher.py` | Teacher dashboard queries |
| `storage/repositories/settings.py` | system_settings CRUD |

### Конфигурация

Добавить в `config.py` (pydantic-settings):
- `SECRET_KEY: str` — обязательное, `ValidationError` при пустом
- `ACCESS_TOKEN_EXPIRE_MINUTES: int` — `> 0`, `ValidationError` при `<= 0`
- `ALGORITHM = "HS256"` — константа в коде (`auth_service.py`), не конфигурируется

### Зависимости (через `uv add`)

```
uv add passlib[bcrypt] python-jose[cryptography]
uv add --group dev pytest-asyncio httpx
```

## Требования безопасности (sharp-edges)

- JWT-алгоритм — только `HS256`, константа; при decode `algorithms=["HS256"]` явно, никогда не из заголовка токена
- `SECRET_KEY` — обязательное поле, пустая строка поднимает `ValidationError` при старте
- `ACCESS_TOKEN_EXPIRE_MINUTES > 0` — валидируется при старте
- `verify_password` — проверять наличие хеша перед bcrypt-сравнением; `True` при пустом хеше недопустим
- Алгоритм хеширования паролей — bcrypt, не конфигурируется

## Порядок выполнения

```
Задача 03 (схема)
    ↓
Задача 04 (endpoints + миграции DDL)
    ↓              ↓
Задача 05       Задача 06
(mock-данные)   (teacher seed)
```

## Применяемые навыки

| Skill | Применение |
|-------|-----------|
| `api-design-principles` | Коды, формат ошибок, пагинация, ресурсы |
| `fastapi-templates` | Depends, service layer, response_model |
| `modern-python` | `uv add`, dependency-groups, Makefile |
| `postgresql-table-design` | Типы, NOT NULL, FK-индексы, CHECK |
| `sharp-edges` | JWT, пароли, конфиги |

## Definition of Done (итерация)

Статус на **2026-04-12** — см. [summary.md](summary.md).

- [x] Все endpoints из Итерации 0 доступны в OpenAPI `/docs`
- [x] JWT-защита работает: без токена — `401`
- [x] `alembic upgrade head` применяется без ошибок
- [x] `make check` / тесты backend — зелёные (зафиксировано в summary)
- [x] Данные для проверки teacher-flow: сид + `GET /v1/teacher/schedule` и связанные вызовы (непустые при наличии seed-занятия)
- [x] `POST /v1/auth/login` с данными преподавателя → `200` + JWT в cookie
- [ ] `docs/data-model.md` — поддерживать в соответствии с миграциями при изменениях схемы
- [ ] `docs/tech/api-contracts.md` — при необходимости догнать под OpenAPI (отдельная задача документации)
