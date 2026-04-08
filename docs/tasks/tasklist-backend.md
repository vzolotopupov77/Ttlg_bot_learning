# Backend Tasklist

## Обзор

**Backend** — ядро системы: клиенты (Telegram-бот, веб) ходят только в API; интеграции (PostgreSQL, LLM, при необходимости Telegram Bot API для исходящих сообщений) подключаются из backend. Этот тасклист описывает **текущий этап**: ядро, диалог ученика с ассистентом («как решить задачу / объяснить тему»), рефакторинг бота на вызовы API, базовое качество.

**Skills:** на этапах выбора стека и проектирования API уместно выполнить `/find-skills` и при необходимости подключить релевантные skills (шаблоны FastAPI, ORM, контракты REST).

Дорожная карта по итерациям продукта — [plan.md](../plan.md). Детализация следующих блоков backend — в отдельных файлах: [tasklist-backend-iteration-4-schedule-hw.md](tasklist-backend-iteration-4-schedule-hw.md), [tasklist-backend-iteration-6-progress.md](tasklist-backend-iteration-6-progress.md).

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

## Связь с plan.md

| Итерация plan.md | Содержание этого тасклиста |
|------------------|----------------------------|
| [Итерация 2: Backend Core](../plan.md#итерация-2-backend-core) | Этапы 1–6, задачи 01–16 |
| [Итерация 3: Персонализированный диалог](../plan.md#итерация-3-персонализированный-диалог) | Задачи 13 (контекст), 17–18 (бот через API) |
| Итерации 4–6 | См. отдельные tasklist'ы; здесь только перекрёстные документы |

---

## Сводная таблица задач

| № | Этап | Описание | Статус | Документы |
|---|------|----------|--------|-----------|
| 01 | 1 | Согласовать и зафиксировать backend-стек | ✅ Done | [план](impl/backend/tasks/task-01-stack/plan.md) \| [summary](impl/backend/tasks/task-01-stack/summary.md) |
| 02 | 1 | ADR: ORM, миграции, тестовый раннер | ✅ Done | [план](impl/backend/tasks/task-02-adr-orm-tests/plan.md) \| [summary](impl/backend/tasks/task-02-adr-orm-tests/summary.md) |
| 03 | 1 | Обновить `.cursor/rules/conventions.mdc` под стек | ✅ Done | [план](impl/backend/tasks/task-03-conventions/plan.md) \| [summary](impl/backend/tasks/task-03-conventions/summary.md) |
| 04 | 2 | API-контракт сценария диалога (`POST /v1/.../message`) | ✅ Done | [план](impl/backend/tasks/task-04-api-dialogue-contract/plan.md) \| [summary](impl/backend/tasks/task-04-api-dialogue-contract/summary.md) |
| 05 | 2 | Конвенции API: префикс, ошибки, коды | ✅ Done | [план](impl/backend/tasks/task-05-api-conventions/plan.md) \| [summary](impl/backend/tasks/task-05-api-conventions/summary.md) |
| 06 | 3 | Каркас `backend/`, FastAPI, `/health` | ✅ Done | [план](impl/backend/tasks/task-06-scaffold/plan.md) \| [summary](impl/backend/tasks/task-06-scaffold/summary.md) |
| 07 | 3 | Конфиг, async PostgreSQL, логирование | ✅ Done | [план](impl/backend/tasks/task-07-config-db-logging/plan.md) \| [summary](impl/backend/tasks/task-07-config-db-logging/summary.md) |
| 08 | 4 | Pytest + тестовая БД / фикстуры | ✅ Done | [план](impl/backend/tasks/task-08-test-harness/plan.md) \| [summary](impl/backend/tasks/task-08-test-harness/summary.md) |
| 09 | 4 | Smoke API-тесты сценариев сообщений (как в боте) | ✅ Done | [план](impl/backend/tasks/task-09-api-smoke-tests/plan.md) \| [summary](impl/backend/tasks/task-09-api-smoke-tests/summary.md) |
| 10 | 5 | ORM-модели и миграции по [data-model.md](../data-model.md) | ✅ Done | [план](impl/backend/tasks/task-10-orm-migrations/plan.md) \| [summary](impl/backend/tasks/task-10-orm-migrations/summary.md) |
| 11 | 5 | CRUD API для доменных сущностей | ✅ Done | [план](impl/backend/tasks/task-11-crud-api/plan.md) \| [summary](impl/backend/tasks/task-11-crud-api/summary.md) |
| 12 | 5 | LLM-клиент OpenRouter + сервис промпта | ✅ Done | [план](impl/backend/tasks/task-12-llm/plan.md) \| [summary](impl/backend/tasks/task-12-llm/summary.md) |
| 13 | 5 | Эндпоинт диалога: контекст, LLM, `Dialogue`/`Message` | ✅ Done | [план](impl/backend/tasks/task-13-dialogue-endpoint/plan.md) \| [summary](impl/backend/tasks/task-13-dialogue-endpoint/summary.md) |
| 14 | 6 | Бот: HTTP-клиент backend; убрать прямой LLM | ✅ Done | [план](impl/backend/tasks/task-14-bot-client/plan.md) \| [summary](impl/backend/tasks/task-14-bot-client/summary.md) |
| 15 | 6 | Интеграционный smoke: bot → backend | ✅ Done | [план](impl/backend/tasks/task-15-integration-smoke/plan.md) \| [summary](impl/backend/tasks/task-15-integration-smoke/summary.md) |
| 16 | 7 | OpenAPI `/docs`, описания схем | ✅ Done | [план](impl/backend/tasks/task-16-openapi-docs/plan.md) \| [summary](impl/backend/tasks/task-16-openapi-docs/summary.md) |
| 17 | 7 | `.env.example`: все переменные backend | ✅ Done | [план](impl/backend/tasks/task-17-env-example/plan.md) \| [summary](impl/backend/tasks/task-17-env-example/summary.md) |
| 18 | 7 | README, vision, plan, integrations — актуализация | ✅ Done | [план](impl/backend/tasks/task-18-docs-sync/plan.md) \| [summary](impl/backend/tasks/task-18-docs-sync/summary.md) |
| 19 | 8 | Ruff, форматирование, цели `Makefile` | ✅ Done | [план](impl/backend/tasks/task-19-lint-format/plan.md) \| [summary](impl/backend/tasks/task-19-lint-format/summary.md) |
| 20 | 8 | Таймауты, fallback, логи без секретов | ✅ Done | [план](impl/backend/tasks/task-20-resilience-logging/plan.md) \| [summary](impl/backend/tasks/task-20-resilience-logging/summary.md) |
| 21 | 9 | Профиль ученика + длительность занятия ([data-model.md](../data-model.md)) | ✅ Done | [итерация 9](impl/backend/iteration-9-student-profile-lesson-duration/plan.md) \| [summary итерации](impl/backend/iteration-9-student-profile-lesson-duration/summary.md) \| [task-21](impl/backend/iteration-9-student-profile-lesson-duration/tasks/task-21-user-profile-lesson-duration/summary.md) |

---

## Итерация 9 — Профиль ученика и длительность занятия

Кратко: расширение `users` и `lessons`, Alembic `a3f8c91d2b04`, API и документация. См. [plan](impl/backend/iteration-9-student-profile-lesson-duration/plan.md).

---

## Этап 1 — Выбор стека и фиксация конвенций

**Skills:** `/find-skills` (FastAPI, SQLAlchemy, Alembic, uv/pytest).

### Задача 01: Согласовать и зафиксировать backend-стек ✅

#### Цель

Определены версии и пакеты: веб-фреймворк (ориентир — FastAPI), async-доступ к PostgreSQL, ORM, миграции (ориентир — Alembic), тесты (pytest + httpx/TestClient). Согласовано с [vision.md](../vision.md) и [ADR-001](../adr/adr-001-database.md).

#### Состав работ

- [x] Зафиксировать список зависимостей в `pyproject.toml` / workspace uv
- [x] Уточнить структуру `backend/src/ttlg_backend/` (`api/`, `services/`, `storage/`, `llm/`)
- [x] Актуализировать таблицу технологий в [docs/vision.md](../vision.md) при отличиях от черновика

#### Definition of Done

**Агент:**

- [x] В `docs/` нет противоречий: стек в vision соответствует принятым решениям
- [x] Есть ссылка на ADR или явная запись в summary задачи при новом решении

**Пользователь:**

- [x] Прочитать summary задачи 01 и при необходимости vision — стек понятен

#### Артефакты

- `docs/vision.md`, при необходимости новый файл в `docs/adr/`

#### Документы

- ✅ [План](impl/backend/tasks/task-01-stack/plan.md)
- ✅ [Summary](impl/backend/tasks/task-01-stack/summary.md)

---

### Задача 02: ADR — ORM, миграции, тестовый раннер ✅

#### Цель

Зафиксированы выбор ORM, инструмента миграций и способа изоляции тестовой БД; обоснование в ADR при отклонении от ориентиров vision.

#### Состав работ

- [x] Создать/обновить ADR в `docs/adr/`
- [x] При необходимости обновить [docs/data-model.md](../data-model.md) (только если меняются типы PK/enum и это уже решено) — не требовалось

#### Definition of Done

**Агент:**

- [x] ADR содержит контекст, альтернативы, решение
- [x] Нет «висящих» TODO в ADR без ссылки на следующую задачу

**Пользователь:**

- [x] Открыть ADR и убедиться, что выбор ORM/миграций назван явно

#### Документы

- ✅ [План](impl/backend/tasks/task-02-adr-orm-tests/plan.md)
- ✅ [Summary](impl/backend/tasks/task-02-adr-orm-tests/summary.md)

---

### Задача 03: Обновить `.cursor/rules/conventions.mdc` ✅

#### Цель

Правила Cursor отражают фактический backend-стек (команды uv, слои FastAPI, тесты, формат логов).

#### Состав работ

- [x] Внести правки в [`.cursor/rules/conventions.mdc`](../../.cursor/rules/conventions.mdc)
- [x] Не расширять стек сверх [vision.md](../vision.md) без правки vision

#### Definition of Done

**Агент:**

- [x] В conventions есть явные ориентиры для backend (при появлении кода — пути пакета)
- [x] Нет устаревших утверждений о «только бот без БД», если уже внедрён backend

**Пользователь:**

- [x] Просмотреть diff `conventions.mdc` — правила соответствуют договорённостям команды

#### Документы

- ✅ [План](impl/backend/tasks/task-03-conventions/plan.md)
- ✅ [Summary](impl/backend/tasks/task-03-conventions/summary.md)

### Проверка этапа 1

**Агент:** наличие ADR (если были новые решения), согласованность vision ↔ conventions.

**Пользователь:** открыть `docs/vision.md`, `docs/adr/`, `.cursor/rules/conventions.mdc`.

**Команды:** не обязательны (документы).

**Результат:** зафиксированный стек и правила для агентов/разработчиков.

---

## Этап 2 — Проектирование API-контракта

**Skills:** `/find-skills` (REST API, OpenAPI, версионирование).

Базовый сценарий из [idea.md](../idea.md): ученик **спрашивает ассистента, как решить задачу или объяснить тему** — первый контракт должен это закрывать без лишних сущностей в запросе.

### Задача 04: Контракт эндпоинта диалога ✅

#### Цель

Описан черновик контракта (минимум): идентификация ученика (например `telegram_id` или внутренний `student_id` до полноценной auth), тело сообщения, ответ ассистента, идентификаторы `dialogue_id` при необходимости; ошибки 4xx/5xx.

#### Состав работ

- [x] Зафиксировать путь (ориентир `POST /v1/dialogue/message` или эквивалент под префиксом `/v1`)
- [x] JSON-схемы request/response, примеры
- [x] Добавить раздел **Backend HTTP API** в [docs/integrations.md](../integrations.md) (без дублирования полного OpenAPI — ссылка на `/docs`)

#### Definition of Done

**Агент:**

- [x] В integrations или отдельном `docs/` фрагменте есть одна таблица/список: метод, назначение, основные поля
- [x] Контракт согласован с сущностями `Dialogue` / `Message` из [data-model.md](../data-model.md)

**Пользователь:**

- [x] Прочитать раздел в [docs/integrations.md](../integrations.md) и понять, что отправляет клиент и что получает

#### Документы

- ✅ [План](impl/backend/tasks/task-04-api-dialogue-contract/plan.md)
- ✅ [Summary](impl/backend/tasks/task-04-api-dialogue-contract/summary.md)

---

### Задача 05: Конвенции API (префикс, ошибки, коды) ✅

#### Цель

Единый префикс версии (`/v1`), формат тела ошибки, согласованные HTTP-коды; описание для клиентов бота и будущего веба.

#### Состав работ

- [x] Зафиксировать в `docs/` (например раздел в integrations или `docs/api-conventions.md` по согласованию)
- [x] Учесть преподавателя/ученика как будущие роли — заглушки допустимы

#### Definition of Done

**Агент:**

- [x] Документ содержит пример JSON ошибки и таблицу кодов для типовых случаев
- [x] Ссылка из [docs/integrations.md](../integrations.md) на конвенции

**Пользователь:**

- [x] Открыть документ конвенций и проверить наличие примера ошибки

#### Документы

- ✅ [План](impl/backend/tasks/task-05-api-conventions/plan.md)
- ✅ [Summary](impl/backend/tasks/task-05-api-conventions/summary.md)

### Проверка этапа 2

**Агент:** контракт диалога + конвенции не противоречат друг другу.

**Пользователь:** [docs/integrations.md](../integrations.md), файл конвенций.

**Результат:** готовая спецификация для реализации в этапе 3–5.

---

## Этап 3 — Каркас backend-сервиса

### Задача 06: Инициализация пакета и `/health` ✅

#### Цель

Поднимается приложение FastAPI; есть маршрут проверки готовности (например `GET /health`).

#### Состав работ

- [x] Создать `backend/src/ttlg_backend/`, точка входа ASGI
- [x] Добавить в [Makefile](../../Makefile) цели: `backend-install`, `backend-run` (имена уточнить в репо, но **новые команды фиксировать в Makefile**)

#### Definition of Done

**Агент:**

- [x] Импорт приложения без ошибок; роут `/health` возвращает успешный ответ
- [x] В README или корневом docs указан порт (или «по умолчанию из uvicorn»)

**Пользователь:**

- [x] `make backend-run` (или эквивалент из Makefile после merge)
- [x] Открыть `http://127.0.0.1:<port>/health` — 200 OK

#### Артефакты

- `backend/`, [Makefile](../../Makefile), при необходимости [README.md](../../README.md)

#### Документы

- ✅ [План](impl/backend/tasks/task-06-scaffold/plan.md)
- ✅ [Summary](impl/backend/tasks/task-06-scaffold/summary.md)

---

### Задача 07: Конфиг, БД, логирование ✅

#### Цель

`pydantic-settings`, `DATABASE_URL`, переменные LLM из [vision.md](../vision.md); структурированное логирование без секретов в сообщениях.

#### Состав работ

- [x] Async-подключение к PostgreSQL (или пул) при старте приложения
- [x] Расширить [.env.example](../../.env.example): `DATABASE_URL`, URL/модель LLM, уровень логов
- [x] При необходимости `docker compose` / `make backend-db-up` для локальной БД

#### Definition of Done

**Агент:**

- [x] Приложение стартует с валидным `.env`; при неверном `DATABASE_URL` — понятная ошибка в логе (без пароля целиком)
- [x] `.env.example` без секретов, с комментариями

**Пользователь:**

- [x] Скопировать `.env.example` → `.env`, поднять БД, запустить backend — без падения на конфиге

#### Артефакты

- `.env.example`, `backend/src/ttlg_backend/config.py` (или аналог), Makefile

#### Документы

- ✅ [План](impl/backend/tasks/task-07-config-db-logging/plan.md)
- ✅ [Summary](impl/backend/tasks/task-07-config-db-logging/summary.md)

### Проверка этапа 3

**Агент:** Makefile содержит актуальные цели; `.env.example` полон для backend.

**Пользователь:**

```text
make backend-db-up    # если добавлено
make backend-install
make backend-run
```

Открыть `/health`. **Ожидание:** сервис отвечает, в логе нет токенов.

---

## Этап 4 — Базовые API-тесты

### Задача 08: Окружение pytest ✅

#### Цель

Запуск тестов одной командой; изолированная/транзакционная работа с БД или тестовый контейнер.

#### Состав работ

- [x] Зависимости dev: pytest, httpx (или starlette TestClient), фикстуры приложения
- [x] Цель `make backend-test`

#### Definition of Done

**Агент:**

- [x] `make backend-test` завершается 0 даже при пустом наборе или с одним smoke
- [x] В CI (если есть) команда совпадает с Makefile

**Пользователь:**

- [x] Выполнить `make backend-test` — успех

#### Документы

- ✅ [План](impl/backend/tasks/task-08-test-harness/plan.md)
- ✅ [Summary](impl/backend/tasks/task-08-test-harness/summary.md)

---

### Задача 09: Smoke-тесты сценариев сообщений ✅

#### Цель

Покрыть сценарии **уже доступные через бота**: свободный текст ученика → ответ ассистента (на этапе без LLM — mock; с LLM — opt-in или помеченные integration).

#### Состав работ

- [x] Тесты вызывают HTTP API так же, как будет бот
- [x] Негативные кейсы: пустое тело, неизвестный пользователь — по конвенции ошибок

#### Definition of Done

**Агент:**

- [x] Минимум два теста: успех и ошибка клиента
- [x] Нет хардкода секретов; ключи из env для integration

**Пользователь:**

- [x] `make backend-test` — все зелёные

#### Документы

- ✅ [План](impl/backend/tasks/task-09-api-smoke-tests/plan.md)
- ✅ [Summary](impl/backend/tasks/task-09-api-smoke-tests/summary.md)

### Проверка этапа 4 (самопроверка)

**Агент:**

- [x] `make backend-test` завершается с кодом 0 (8 passed)
- [x] Нет ошибок импорта в `backend/tests/`
- [x] Способ mock LLM задокументирован в [плане задачи 09](impl/backend/tasks/task-09-api-smoke-tests/plan.md) и в `conftest.py` (фикстура `dialogue_client`)
- [x] В [backend/pyproject.toml](../../backend/pyproject.toml) объявлены dev-зависимости: `pytest`, `pytest-asyncio`, `httpx`
- [x] Тесты не флаки на повторных прогонах (autouse-сброс состояния, `@pytest.mark.asyncio` убран — `asyncio_mode=auto`)

**Пользователь:**

- [x] `make backend-test` — 16 passed (этап 5 расширил suite с 8 до 16 тестов)
- [x] `make backend-test` без запущенной БД — `GET /health` возвращает **503** degraded

**Результат:** регрессия по контракту диалога ловится автоматически.

**План итерации:** [impl/backend/iteration-4-tests/plan.md](impl/backend/iteration-4-tests/plan.md).

---

## Этап 5 — Эндпоинты и серверная логика

### Задача 10: ORM и миграции ✅

#### Цель

Таблицы соответствуют [data-model.md](../data-model.md) (`User`, `Lesson`, `Assignment`, `Progress`, `Dialogue`, `Message`); миграции применимы с нуля.

#### Состав работ

- [x] Модели и связи в `storage/`; Alembic (или выбранный инструмент)
- [x] При отличии схемы от документа — обновить [docs/data-model.md](../data-model.md) и зафиксировать в summary (отклонение зафиксировано в summary: PK = UUID)

#### Definition of Done

**Агент:**

- [x] `alembic upgrade head` (или аналог) без ошибок на чистой БД
- [x] Enum и FK согласованы с документом

**Пользователь:**

- [x] Миграция проверена через SQLite (`TTLG_ALLOW_SQLITE_TEST=1`); схема создаётся при старте сервера

#### Документы

- ✅ [План](impl/backend/tasks/task-10-orm-migrations/plan.md)
- ✅ [Summary](impl/backend/tasks/task-10-orm-migrations/summary.md)

---

### Задача 11: CRUD API ✅

#### Цель

Базовые операции для сущностей из data-model; валидация Pydantic; заготовка проверок по ролям (хотя бы dependency placeholder).

#### Состав работ

- [x] Роутеры, сервисы, репозитории
- [x] Актуализировать OpenAPI после добавления роутов

#### Definition of Done

**Агент:**

- [x] Smoke или тесты на create/read для каждой сущности (или согласованный минимум)
- [x] Нет дублирования бизнес-логики в роутерах сверх тривиального

**Пользователь:**

- [x] `/docs` открыт; роуты `/v1/users`, `/v1/lessons`, `/v1/assignments`, `/v1/dialogue/message` присутствуют

#### Документы

- ✅ [План](impl/backend/tasks/task-11-crud-api/plan.md)
- ✅ [Summary](impl/backend/tasks/task-11-crud-api/summary.md)

---

### Задача 12: LLM-клиент и промпт ✅

#### Цель

Вызов OpenRouter через OpenAI-compatible клиент; `base_url`, модель, ключ из конфига; сборка системного сообщения + контекст ученика + вопрос.

#### Состав работ

- [x] Модуль `llm/`; таймаут и обработка ошибок провайдера
- [x] Синхронизировать детали с [docs/integrations.md](../integrations.md) (этап 6 / по необходимости)

#### Definition of Done

**Агент:**

- [x] Юнит-тест с моком HTTP к провайдеру или записанным ответом
- [x] В логах нет `OPENROUTER_API_KEY` и полного промпта с персональными данными в production-уровне

**Пользователь:**

- [x] Ручной запрос к диалогу с `OPENROUTER_API_KEY` — осмысленный ответ от `openai/gpt-4o-mini` получен (2026-03-30)

#### Документы

- ✅ [План](impl/backend/tasks/task-12-llm/plan.md)
- ✅ [Summary](impl/backend/tasks/task-12-llm/summary.md)

---

### Задача 13: Эндпоинт диалога (полный сценарий) ✅

#### Цель

Реализован контракт задачи 04: сохранение сообщений, вызов LLM, ответ клиенту; контекст из БД (занятия, ДЗ) подмешивается, когда данные есть.

#### Состав работ

- [x] Связать сервис диалога с репозиториями `Dialogue`/`Message`
- [x] Сверить ответы с [tasklist-bot-iteration-3-personalized-dialog.md](tasklist-bot-iteration-3-personalized-dialog.md) при необходимости (итерация бота)

#### Definition of Done

**Агент:**

- [x] Тесты задачи 09 проходят против реальной реализации
- [x] История переписки сохраняется в БД

**Пользователь:**

- [x] Запрос через PowerShell к `POST /v1/dialogue/message` — ответ и сохранение `dialogue_id` проверены (SQLite-файл, 2026-03-30)

#### Документы

- ✅ [План](impl/backend/tasks/task-13-dialogue-endpoint/plan.md)
- ✅ [Summary](impl/backend/tasks/task-13-dialogue-endpoint/summary.md)

### Проверка этапа 5 (самопроверка)

**Агент:**

- [x] `make backend-test` — 16 passed (диалог, CRUD smoke, LLM mock, health, 503 LLM)
- [x] Миграция `backend/alembic/versions/0001_initial_schema.py`; команда `make backend-db-migrate`
- [x] OpenAPI: роуты `/v1/users`, `/v1/lessons`, `/v1/assignments`, `/v1/dialogue/message`
- [x] `telegram_id` bigint; PK UUID (зафиксировано в summary задачи 10)

**Пользователь:**

- [x] `make backend-test` — 16 passed (2026-03-30)
- [x] `/health`, `POST /v1/users`, `POST /v1/dialogue/message` (новый и продолжение диалога) — проверены вручную
- [x] LLM-ответ получен от `openai/gpt-4o-mini` через OpenRouter

> Проверка выполнена с SQLite-файлом (без PostgreSQL). Проверка с PostgreSQL откладывается до этапа 6/7.

**Результаты фиксированы:** [iteration-5-endpoints/summary.md](impl/backend/iteration-5-endpoints/summary.md)

**План итерации:** [impl/backend/iteration-5-endpoints/plan.md](impl/backend/iteration-5-endpoints/plan.md).

---

## Этап 6 — Рефакторинг клиента (бота)

### Задача 14: Бот как тонкий клиент ✅

#### Цель

Исходящий путь: **Update → handler → backend HTTP API**; прямых вызовов LLM из бота нет. Ориентир: `src/ttlg_bot/services/backend_client.py` (или согласованный путь из [vision.md](../vision.md)).

#### Состав работ

- [x] Конфиг URL backend и таймауты
- [x] Удалить/отключить старый LLM-клиент из бота
- [x] Обновить [docs/vision.md](../vision.md), если фактическая структура пакета бота изменилась

#### Definition of Done

**Агент:**

- [x] В коде бота нет импорта OpenAI/OpenRouter SDK (кроме тестовых заглушек)
- [x] Ошибки backend маппятся в короткое сообщение пользователю

**Пользователь:**

- [x] Запустить только backend + бот; в Telegram отправить текст — ответ приходит (2026-03-31)

#### Документы

- ✅ [План](impl/backend/tasks/task-14-bot-client/plan.md)
- ✅ [Summary](impl/backend/tasks/task-14-bot-client/summary.md)

---

### Задача 15: Интеграционный smoke ✅

#### Цель

Один сценарий «как у пользователя»: бот → backend → (mock/real LLM) → ответ в чат.

#### Состав работ

- [x] Документировать в README команду или скрипт smoke (опционально `make smoke-integration`)
- [x] При необходимости добавить pytest с поднятием обоих процессов (опционально, не блокер MVP)

#### Definition of Done

**Агент:**

- [x] Чек-лист ручной проверки записан в summary или README
- [x] Нет регрессии `make backend-test`

**Пользователь:**

- [x] Выполнить ручной smoke по README (2026-03-31)

#### Документы

- ✅ [План](impl/backend/tasks/task-15-integration-smoke/plan.md)
- ✅ [Summary](impl/backend/tasks/task-15-integration-smoke/summary.md)

### Проверка этапа 6 (самопроверка)

**Агент:**

- [x] В `src/` нет вхождений `openai` / `AsyncOpenAI` (`rg`)
- [x] `make backend-test` — 16 passed (регрессии нет; попутно исправлен `test_health_without_database_returns_503`)
- [x] `make bot-test` — 7 passed (интеграционные тесты `BackendClient → ASGITransport → backend`)
- [x] Паттерн `httpx.AsyncClient(transport=ASGITransport(app=app))` покрывает: успех, `dialogue_id` continuity, `user_not_found`, `llm_unavailable`, `ConnectError`, `dialogue_not_found`
- [x] `BackendClient` принимает `_client` для инъекции в тестах; prod-код не изменился
- [x] `uv run python -c "import ttlg_bot"` — без ошибок

**Пользователь:**

```text
make backend-run   # терминал 1
make run           # терминал 2
```

Telegram: `/start` и произвольное сообщение. **Ожидание:** ответ из backend.

- [x] Ручной smoke пройден (2026-03-31): SQLite, backend + бот, LLM-ответ в Telegram — ✓; BACKEND_TIMEOUT скорректирован до 90s

**Результаты фиксированы:** [iteration-6-bot-client/summary.md](impl/backend/iteration-6-bot-client/summary.md)

**План итерации:** [impl/backend/iteration-6-bot-client/plan.md](impl/backend/iteration-6-bot-client/plan.md).

---

## Этап 7 — Документирование backend

**План итерации:** [impl/backend/iteration-7-backend-docs/plan.md](impl/backend/iteration-7-backend-docs/plan.md).

### Задача 16: OpenAPI и `/docs` ✅

#### Цель

Swagger/OpenAPI отражает все публичные роуты; описания полей и примеры где уместно.

#### Состав работ

- [x] `summary`/`description` у эндпоинтов; теги по областям
- [x] Опционально: `make openapi-export` — выгрузка схемы в `docs/openapi.json`

#### Definition of Done

**Агент:**

- [x] Нет незадокументированных публичных POST/PUT без короткого description
- [x] Версия API в пути соответствует задаче 05

**Пользователь:**

- [x] Открыть `http://127.0.0.1:<port>/docs` — все основные группы на месте (проверено при сценарии SQLite)

#### Документы

- ✅ [План](impl/backend/tasks/task-16-openapi-docs/plan.md)
- ✅ [Summary](impl/backend/tasks/task-16-openapi-docs/summary.md)

---

### Задача 17: `.env.example` ✅

#### Цель

Полный перечень переменных backend с краткими комментариями; те же имена используются в коде.

#### Состав работ

- [x] Сверить с [docs/integrations.md](../integrations.md) и [docs/vision.md](../vision.md)
- [x] Отдельные переменные для тестов (`TTLG_ALLOW_SQLITE_TEST` — закомментирован в `.env.example`)

#### Definition of Done

**Агент:**

- [x] Нет переменной в коде, которой нет в `.env.example`
- [x] В README есть отсылка к `.env.example`

**Пользователь:**

- [x] Заполнить `.env` только по примеру — сервис и тесты стартуют (backend + бот на SQLite по README)

#### Документы

- ✅ [План](impl/backend/tasks/task-17-env-example/plan.md)
- ✅ [Summary](impl/backend/tasks/task-17-env-example/summary.md)

---

### Задача 18: Синхронизация документации ✅

#### Цель

Актуальны: [README.md](../../README.md), [docs/vision.md](../vision.md), [docs/plan.md](../plan.md), [docs/data-model.md](../data-model.md), [docs/integrations.md](../integrations.md) — только факты о реализованном backend и запуске.

#### Состав работ

- [x] README: последовательность «БД → backend → бот»; команды Makefile
- [x] plan.md: статусы итераций 2–3 при достижении вех (без расширения scope)

#### Definition of Done

**Агент:**

- [x] Пройтись чек-листом файлов; нет ссылок на несуществующие команды
- [x] vision отражает «тонкие клиенты» при готовности задачи 14

**Пользователь:**

- [x] Зайти с нуля в репо по README — окружение поднимается (ветка **без PostgreSQL**: SQLite + `TTLG_ALLOW_SQLITE_TEST=1`, см. README)

#### Документы

- ✅ [План](impl/backend/tasks/task-18-docs-sync/plan.md)
- ✅ [Summary](impl/backend/tasks/task-18-docs-sync/summary.md)

### Проверка этапа 7 (самопроверка)

**Агент:**

- [x] `make backend-test` — 16 passed
- [x] Нет `openai` / `AsyncOpenAI` в `src/ttlg_bot` (тонкий клиент сохранён)
- [x] `make openapi-export` создаёт [docs/openapi.json](../openapi.json)
- [x] README, `plan.md`, `vision.md`, `integrations.md`, `.env.example` согласованы с Makefile

**Пользователь:**

- [x] README end-to-end (SQLite); открыть `/docs`

**Результаты фиксированы:** [iteration-7-backend-docs/summary.md](impl/backend/iteration-7-backend-docs/summary.md)

---

## Этап 8 — Качество и инженерные практики

### Задача 19: Линт и формат ✅

#### Цель

Единый стиль: Ruff (lint + format или согласованный split); цели `make lint`, `make format`, при необходимости `make check` (линт + тесты).

#### Состав работ

- [x] Конфиг Ruff в репозитории
- [x] Обновить [Makefile](../../Makefile) и [README.md](../../README.md)

#### Definition of Done

**Агент:**

- [x] `make lint` и `make format` завершаются без ошибок на чистом дереве
- [x] Игноры обоснованы в `pyproject` или ruff.toml

**Пользователь:**

- [x] Запустить `make lint` перед PR

#### Документы

- ✅ [План](impl/backend/tasks/task-19-lint-format/plan.md)
- ✅ [Summary](impl/backend/tasks/task-19-lint-format/summary.md)

---

### Задача 20: Устойчивость и логи ✅

#### Цель

Таймауты на HTTP к LLM и к backend из бота; при сбое — краткий текст пользователю; логи без токенов и PII.

#### Состав работ

- [x] Проверить все внешние вызовы (бот ↔ backend, backend ↔ OpenRouter)
- [x] Актуализировать раздел безопасности в [docs/vision.md](../vision.md) при новых правилах

#### Definition of Done

**Агент:**

- [x] Искусственно обрубить сеть к LLM — сервис не падает, пользователь видит fallback
- [x] В логе нет полного Authorization header

**Пользователь:**

- [x] Симулировать неверный ключ API — понятное сообщение в Telegram (в Telegram: обобщённый текст «Ассистент временно недоступен…»; детали — в логах админа)

#### Документы

- ✅ [План](impl/backend/tasks/task-20-resilience-logging/plan.md)
- ✅ [Summary](impl/backend/tasks/task-20-resilience-logging/summary.md)

### Проверка этапа 8 (самопроверка)

**Агент:**

- [x] `make lint` — без ошибок
- [x] `make format` — код отформатирован (при необходимости прогнать перед коммитом)
- [x] `make backend-test` — зелёный (17 passed)
- [x] `make bot-test` — зелёный (7 passed)
- [x] `make check` — линт + оба набора тестов
- [x] Тест `test_llm_client_api_error_does_not_log_secret_key` — в логах нет ключа и строки `Authorization`
- [x] Итоги итерации: [iteration-8-quality/summary.md](impl/backend/iteration-8-quality/summary.md)

**Пользователь:**

- [x] Перед PR: `make lint` или `make check`
- [x] Ручная проверка: backend без сети к OpenRouter / неверный ключ — бот не падает, в чате краткое сообщение

**Команды:**

```text
make lint
make check
```

**Результат:** репозиторий готов к расширению API (расписание, ДЗ — см. отдельные tasklist'ы).

---

## Дальнейшие итерации backend (вне текущего этапа)

| Тема | Документ |
|------|----------|
| Расписание, ДЗ, напоминания | [tasklist-backend-iteration-4-schedule-hw.md](tasklist-backend-iteration-4-schedule-hw.md) |
| Прогресс и аналитика | [tasklist-backend-iteration-6-progress.md](tasklist-backend-iteration-6-progress.md) |

При появлении новых команд локального запуска, проверки и обслуживания — **добавлять или обновлять цели в [Makefile](../../Makefile)** и одну строку в [README.md](../../README.md).
