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
| 06 | 3 | Каркас `backend/`, FastAPI, `/health` | 📋 Planned | [план](impl/backend/tasks/task-06-scaffold/plan.md) \| [summary](impl/backend/tasks/task-06-scaffold/summary.md) |
| 07 | 3 | Конфиг, async PostgreSQL, логирование | 📋 Planned | [план](impl/backend/tasks/task-07-config-db-logging/plan.md) \| [summary](impl/backend/tasks/task-07-config-db-logging/summary.md) |
| 08 | 4 | Pytest + тестовая БД / фикстуры | 📋 Planned | [план](impl/backend/tasks/task-08-test-harness/plan.md) \| [summary](impl/backend/tasks/task-08-test-harness/summary.md) |
| 09 | 4 | Smoke API-тесты сценариев сообщений (как в боте) | 📋 Planned | [план](impl/backend/tasks/task-09-api-smoke-tests/plan.md) \| [summary](impl/backend/tasks/task-09-api-smoke-tests/summary.md) |
| 10 | 5 | ORM-модели и миграции по [data-model.md](../data-model.md) | 📋 Planned | [план](impl/backend/tasks/task-10-orm-migrations/plan.md) \| [summary](impl/backend/tasks/task-10-orm-migrations/summary.md) |
| 11 | 5 | CRUD API для доменных сущностей | 📋 Planned | [план](impl/backend/tasks/task-11-crud-api/plan.md) \| [summary](impl/backend/tasks/task-11-crud-api/summary.md) |
| 12 | 5 | LLM-клиент OpenRouter + сервис промпта | 📋 Planned | [план](impl/backend/tasks/task-12-llm/plan.md) \| [summary](impl/backend/tasks/task-12-llm/summary.md) |
| 13 | 5 | Эндпоинт диалога: контекст, LLM, `Dialogue`/`Message` | 📋 Planned | [план](impl/backend/tasks/task-13-dialogue-endpoint/plan.md) \| [summary](impl/backend/tasks/task-13-dialogue-endpoint/summary.md) |
| 14 | 6 | OpenAPI `/docs`, описания схем | 📋 Planned | [план](impl/backend/tasks/task-14-openapi-docs/plan.md) \| [summary](impl/backend/tasks/task-14-openapi-docs/summary.md) |
| 15 | 6 | `.env.example`: все переменные backend | 📋 Planned | [план](impl/backend/tasks/task-15-env-example/plan.md) \| [summary](impl/backend/tasks/task-15-env-example/summary.md) |
| 16 | 6 | README, vision, plan, integrations — актуализация | 📋 Planned | [план](impl/backend/tasks/task-16-docs-sync/plan.md) \| [summary](impl/backend/tasks/task-16-docs-sync/summary.md) |
| 17 | 7 | Бот: HTTP-клиент backend; убрать прямой LLM | 📋 Planned | [план](impl/backend/tasks/task-17-bot-client/plan.md) \| [summary](impl/backend/tasks/task-17-bot-client/summary.md) |
| 18 | 7 | Интеграционный smoke: bot → backend | 📋 Planned | [план](impl/backend/tasks/task-18-integration-smoke/plan.md) \| [summary](impl/backend/tasks/task-18-integration-smoke/summary.md) |
| 19 | 8 | Ruff, форматирование, цели `Makefile` | 📋 Planned | [план](impl/backend/tasks/task-19-lint-format/plan.md) \| [summary](impl/backend/tasks/task-19-lint-format/summary.md) |
| 20 | 8 | Таймауты, fallback, логи без секретов | 📋 Planned | [план](impl/backend/tasks/task-20-resilience-logging/plan.md) \| [summary](impl/backend/tasks/task-20-resilience-logging/summary.md) |

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

- [ ] Прочитать summary задачи 01 и при необходимости vision — стек понятен

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

- [ ] Открыть ADR и убедиться, что выбор ORM/миграций назван явно

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

- [ ] Просмотреть diff `conventions.mdc` — правила соответствуют договорённостям команды

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

- [ ] Прочитать раздел в [docs/integrations.md](../integrations.md) и понять, что отправляет клиент и что получает

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

- [ ] Открыть документ конвенций и проверить наличие примера ошибки

#### Документы

- ✅ [План](impl/backend/tasks/task-05-api-conventions/plan.md)
- ✅ [Summary](impl/backend/tasks/task-05-api-conventions/summary.md)

### Проверка этапа 2

**Агент:** контракт диалога + конвенции не противоречат друг другу.

**Пользователь:** [docs/integrations.md](../integrations.md), файл конвенций.

**Результат:** готовая спецификация для реализации в этапе 3–5.

---

## Этап 3 — Каркас backend-сервиса

### Задача 06: Инициализация пакета и `/health` 📋

#### Цель

Поднимается приложение FastAPI; есть маршрут проверки готовности (например `GET /health`).

#### Состав работ

- [ ] Создать `backend/src/ttlg_backend/`, точка входа ASGI
- [ ] Добавить в [Makefile](../../Makefile) цели: `backend-install`, `backend-run` (имена уточнить в репо, но **новые команды фиксировать в Makefile**)

#### Definition of Done

**Агент:**

- [ ] Импорт приложения без ошибок; роут `/health` возвращает успешный ответ
- [ ] В README или корневом docs указан порт (или «по умолчанию из uvicorn»)

**Пользователь:**

- [ ] `make backend-run` (или эквивалент из Makefile после merge)
- [ ] Открыть `http://127.0.0.1:<port>/health` — 200 OK

#### Артефакты

- `backend/`, [Makefile](../../Makefile), при необходимости [README.md](../../README.md)

#### Документы

- 📋 [План](impl/backend/tasks/task-06-scaffold/plan.md)
- 📝 [Summary](impl/backend/tasks/task-06-scaffold/summary.md)

---

### Задача 07: Конфиг, БД, логирование 📋

#### Цель

`pydantic-settings`, `DATABASE_URL`, переменные LLM из [vision.md](../vision.md); структурированное логирование без секретов в сообщениях.

#### Состав работ

- [ ] Async-подключение к PostgreSQL (или пул) при старте приложения
- [ ] Расширить [.env.example](../../.env.example): `DATABASE_URL`, URL/модель LLM, уровень логов
- [ ] При необходимости `docker compose` / `make backend-db-up` для локальной БД

#### Definition of Done

**Агент:**

- [ ] Приложение стартует с валидным `.env`; при неверном `DATABASE_URL` — понятная ошибка в логе (без пароля целиком)
- [ ] `.env.example` без секретов, с комментариями

**Пользователь:**

- [ ] Скопировать `.env.example` → `.env`, поднять БД, запустить backend — без падения на конфиге

#### Артефакты

- `.env.example`, `backend/src/ttlg_backend/config.py` (или аналог), Makefile

#### Документы

- 📋 [План](impl/backend/tasks/task-07-config-db-logging/plan.md)
- 📝 [Summary](impl/backend/tasks/task-07-config-db-logging/summary.md)

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

### Задача 08: Окружение pytest 📋

#### Цель

Запуск тестов одной командой; изолированная/транзакционная работа с БД или тестовый контейнер.

#### Состав работ

- [ ] Зависимости dev: pytest, httpx (или starlette TestClient), фикстуры приложения
- [ ] Цель `make backend-test`

#### Definition of Done

**Агент:**

- [ ] `make backend-test` завершается 0 даже при пустом наборе или с одним smoke
- [ ] В CI (если есть) команда совпадает с Makefile

**Пользователь:**

- [ ] Выполнить `make backend-test` — успех

#### Документы

- 📋 [План](impl/backend/tasks/task-08-test-harness/plan.md)
- 📝 [Summary](impl/backend/tasks/task-08-test-harness/summary.md)

---

### Задача 09: Smoke-тесты сценариев сообщений 📋

#### Цель

Покрыть сценарии **уже доступные через бота**: свободный текст ученика → ответ ассистента (на этапе без LLM — mock; с LLM — opt-in или помеченные integration).

#### Состав работ

- [ ] Тests вызывают HTTP API так же, как будет бот
- [ ] Негативные кейсы: пустое тело, неизвестный пользователь — по конвенции ошибок

#### Definition of Done

**Агент:**

- [ ] Минимум два теста: успех и ошибка клиента
- [ ] Нет хардкода секретов; ключи из env для integration

**Пользователь:**

- [ ] `make backend-test` — все зелёные

#### Документы

- 📋 [План](impl/backend/tasks/task-09-api-smoke-tests/plan.md)
- 📝 [Summary](impl/backend/tasks/task-09-api-smoke-tests/summary.md)

### Проверка этапа 4

**Агент:** тесты не флаки, документирован способ mock LLM.

**Пользователь:** `make backend-test`.

**Результат:** регрессия по контракту диалога ловится автоматически.

---

## Этап 5 — Эндпоинты и серверная логика

### Задача 10: ORM и миграции 📋

#### Цель

Таблицы соответствуют [data-model.md](../data-model.md) (`User`, `Lesson`, `Assignment`, `Progress`, `Dialogue`, `Message`); миграции применимы с нуля.

#### Состав работ

- [ ] Модели и связи в `storage/`; Alembic (или выбранный инструмент)
- [ ] При отличии схемы от документа — обновить [docs/data-model.md](../data-model.md) и зафиксировать в summary

#### Definition of Done

**Агент:**

- [ ] `alembic upgrade head` (или аналог) без ошибок на чистой БД
- [ ] Enum и FK согласованы с документом

**Пользователь:**

- [ ] По инструкции в README применить миграции и убедиться, что таблицы созданы

#### Документы

- 📋 [План](impl/backend/tasks/task-10-orm-migrations/plan.md)
- 📝 [Summary](impl/backend/tasks/task-10-orm-migrations/summary.md)

---

### Задача 11: CRUD API 📋

#### Цель

Базовые операции для сущностей из data-model; валидация Pydantic; заготовка проверок по ролям (хотя бы dependency placeholder).

#### Состав работ

- [ ] Роутеры, сервисы, репозитории
- [ ] Актуализировать OpenAPI после добавления роутов

#### Definition of Done

**Агент:**

- [ ] Smoke или тесты на create/read для каждой сущности (или согласованный минимум)
- [ ] Нет дублирования бизнес-логики в роутерах сверх тривиального

**Пользователь:**

- [ ] Открыть `/docs`, проверить наличие основных ресурсов

#### Документы

- 📋 [План](impl/backend/tasks/task-11-crud-api/plan.md)
- 📝 [Summary](impl/backend/tasks/task-11-crud-api/summary.md)

---

### Задача 12: LLM-клиент и промпт 📋

#### Цель

Вызов OpenRouter через OpenAI-compatible клиент; `base_url`, модель, ключ из конфига; сборка системного сообщения + контекст ученика + вопрос.

#### Состав работ

- [ ] Модуль `llm/`; таймаут и обработка ошибок провайдера
- [ ] Синхронизировать детали с [docs/integrations.md](../integrations.md)

#### Definition of Done

**Агент:**

- [ ] Юнит-тест с моком HTTP к провайдеру или записанным ответом
- [ ] В логах нет `OPENROUTER_API_KEY` и полного промпта с персональными данными в production-уровне

**Пользователь:**

- [ ] При локальном запуске с ключом — один ручной запрос к тестовому эндпоинту (после задачи 13) возвращает осмысленный ответ

#### Документы

- 📋 [План](impl/backend/tasks/task-12-llm/plan.md)
- 📝 [Summary](impl/backend/tasks/task-12-llm/summary.md)

---

### Задача 13: Эндпоинт диалога (полный сценарий) 📋

#### Цель

Реализован контракт задачи 04: сохранение сообщений, вызов LLM, ответ клиенту; контекст из БД (занятия, ДЗ) подмешивается, когда данные есть.

#### Состав работ

- [ ] Связать сервис диалога с репозиториями `Dialogue`/`Message`
- [ ] Сверить ответы с [tasklist-bot-iteration-3-personalized-dialog.md](tasklist-bot-iteration-3-personalized-dialog.md) при необходимости

#### Definition of Done

**Агент:**

- [ ] Тесты задачи 09 проходят против реальной реализации
- [ ] История переписки сохраняется в БД

**Пользователь:**

- [ ] Через `/docs` выполнить запрос к эндпоинту диалога — ответ и запись в БД

#### Документы

- 📋 [План](impl/backend/tasks/task-13-dialogue-endpoint/plan.md)
- 📝 [Summary](impl/backend/tasks/task-13-dialogue-endpoint/summary.md)

### Проверка этапа 5

**Агент:** CRUD + диалог + миграции; OpenAPI не пустой; data-model в sync.

**Пользователь:**

```text
make backend-test
make backend-run
```

Открыть `/docs`, вызвать диалог и CRUD пример. **Ожидание:** данные в PostgreSQL, ответ ассистента при валидном ключе LLM.

---

## Этап 6 — Документирование backend

### Задача 14: OpenAPI и `/docs` 📋

#### Цель

Swagger/OpenAPI отражает все публичные роуты; описания полей и примеры где уместно.

#### Состав работ

- [ ] `summary`/`description` у эндпоинтов; теги по областям
- [ ] Опционально: `make openapi-export` — выгрузка схемы в `docs/` (если добавят)

#### Definition of Done

**Агент:**

- [ ] Нет незадокументированных публичных POST/PUT без короткого description
- [ ] Версия API в пути соответствует задаче 05

**Пользователь:**

- [ ] Открыть `http://127.0.0.1:<port>/docs` — все основные группы на месте

#### Документы

- 📋 [План](impl/backend/tasks/task-14-openapi-docs/plan.md)
- 📝 [Summary](impl/backend/tasks/task-14-openapi-docs/summary.md)

---

### Задача 15: `.env.example` 📋

#### Цель

Полный перечень переменных backend с краткими комментариями; те же имена используются в коде.

#### Состав работ

- [ ] Сверить с [docs/integrations.md](../integrations.md) и [docs/vision.md](../vision.md)
- [ ] Отдельные переменные для тестов (если нужны)

#### Definition of Done

**Агент:**

- [ ] Нет переменной в коде, которой нет в `.env.example`
- [ ] В README есть отсылка к `.env.example`

**Пользователь:**

- [ ] Заполнить `.env` только по примеру — сервис и тесты стартуют

#### Документы

- 📋 [План](impl/backend/tasks/task-15-env-example/plan.md)
- 📝 [Summary](impl/backend/tasks/task-15-env-example/summary.md)

---

### Задача 16: Синхронизация документации 📋

#### Цель

Актуальны: [README.md](../../README.md), [docs/vision.md](../vision.md), [docs/plan.md](../plan.md), [docs/data-model.md](../data-model.md), [docs/integrations.md](../integrations.md) — только факты о реализованном backend и запуске.

#### Состав работ

- [ ] README: последовательность «БД → backend → бот»; команды Makefile
- [ ] plan.md: статусы итераций 2–3 при достижении вех (без расширения scope)

#### Definition of Done

**Агент:**

- [ ] Пройтись чек-листом файлов; нет ссылок на несуществующие команды
- [ ] vision отражает «тонкие клиенты» при готовности задачи 17

**Пользователь:**

- [ ] Зайти с нуля в репо по README — окружение поднимается

#### Документы

- 📋 [План](impl/backend/tasks/task-16-docs-sync/plan.md)
- 📝 [Summary](impl/backend/tasks/task-16-docs-sync/summary.md)

### Проверка этапа 6

**Агент:** перечисленные md и `.env.example` согласованы.

**Пользователь:** пройти README end-to-end; открыть `/docs`.

---

## Этап 7 — Рефакторинг клиента (бота)

### Задача 17: Бот как тонкий клиент 📋

#### Цель

Исходящий путь: **Update → handler → backend HTTP API**; прямых вызовов LLM из бота нет. Ориентир: `src/ttlg_bot/services/backend_client.py` (или согласованный путь из [vision.md](../vision.md)).

#### Состав работ

- [ ] Конфиг URL backend и таймауты
- [ ] Удалить/отключить старый LLM-клиент из бота
- [ ] Обновить [docs/vision.md](../vision.md), если фактическая структура пакета бота изменилась

#### Definition of Done

**Агент:**

- [ ] В коде бота нет импорта OpenAI/OpenRouter SDK (кроме тестовых заглушек)
- [ ] Ошибки backend маппятся в короткое сообщение пользователю

**Пользователь:**

- [ ] Запустить только backend + бот; в Telegram отправить текст — ответ приходит

#### Документы

- 📋 [План](impl/backend/tasks/task-17-bot-client/plan.md)
- 📝 [Summary](impl/backend/tasks/task-17-bot-client/summary.md)

---

### Задача 18: Интеграционный smoke 📋

#### Цель

Один сценарий «как у пользователя»: бот → backend → (mock/real LLM) → ответ в чат.

#### Состав работ

- [ ] Документировать в README команду или скрипт smoke (опционально `make smoke-integration`)
- [ ] При необходимости добавить pytest с поднятием обоих процессов (опционально, не блокер MVP)

#### Definition of Done

**Агент:**

- [ ] Чек-лист ручной проверки записан в summary или README
- [ ] Нет регрессии `make backend-test`

**Пользователь:**

- [ ] Выполнить ручной smoke по README

#### Документы

- 📋 [План](impl/backend/tasks/task-18-integration-smoke/plan.md)
- 📝 [Summary](impl/backend/tasks/task-18-integration-smoke/summary.md)

### Проверка этапа 7

**Агент:** grep по репо — нет прямого LLM в боте.

**Пользователь:**

```text
make backend-run   # терминал 1
make run           # или make bot-run — как зафиксировано в Makefile, терминал 2
```

Telegram: `/start` и произвольное сообщение. **Ожидание:** ответ как до рефакторинга по UX, источник — backend.

---

## Этап 8 — Качество и инженерные практики

### Задача 19: Линт и формат 📋

#### Цель

Единый стиль: Ruff (lint + format или согласованный split); цели `make lint`, `make format`, при необходимости `make check` (линт + тесты).

#### Состав работ

- [ ] Конфиг Ruff в репозитории
- [ ] Обновить [Makefile](../../Makefile) и [README.md](../../README.md)

#### Definition of Done

**Агент:**

- [ ] `make lint` и `make format` завершаются без ошибок на чистом дереве
- [ ] Игноры обоснованы в `pyproject` или ruff.toml

**Пользователь:**

- [ ] Запустить `make lint` перед PR

#### Документы

- 📋 [План](impl/backend/tasks/task-19-lint-format/plan.md)
- 📝 [Summary](impl/backend/tasks/task-19-lint-format/summary.md)

---

### Задача 20: Устойчивость и логи 📋

#### Цель

Таймауты на HTTP к LLM и к backend из бота; при сбое — краткий текст пользователю; логи без токенов и PII.

#### Состав работ

- [ ] Проверить все внешние вызовы (бот ↔ backend, backend ↔ OpenRouter)
- [ ] Актуализировать раздел безопасности в [docs/vision.md](../vision.md) при новых правилах

#### Definition of Done

**Агент:**

- [ ] Искусственно обрубить сеть к LLM — сервис не падает, пользователь видит fallback
- [ ] В логе нет полного Authorization header

**Пользователь:**

- [ ] Симулировать неверный ключ API — понятное сообщение в Telegram

#### Документы

- 📋 [План](impl/backend/tasks/task-20-resilience-logging/plan.md)
- 📝 [Summary](impl/backend/tasks/task-20-resilience-logging/summary.md)

### Проверка этапа 8

**Агент:** пройти Ruff + тесты; spot-check логов.

**Пользователь:**

```text
make lint
make backend-test
```

**Результат:** репозиторий готов к расширению API (расписание, ДЗ — см. отдельные tasklist'ы).

---

## Дальнейшие итерации backend (вне текущего этапа)

| Тема | Документ |
|------|----------|
| Расписание, ДЗ, напоминания | [tasklist-backend-iteration-4-schedule-hw.md](tasklist-backend-iteration-4-schedule-hw.md) |
| Прогресс и аналитика | [tasklist-backend-iteration-6-progress.md](tasklist-backend-iteration-6-progress.md) |

При появлении новых команд локального запуска, проверки и обслуживания — **добавлять или обновлять цели в [Makefile](../../Makefile)** и одну строку в [README.md](../../README.md).
