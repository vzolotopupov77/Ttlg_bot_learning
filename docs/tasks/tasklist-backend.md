# Backend Tasklist

## Обзор

**Backend** — ядро системы: через него работают все клиенты (Telegram-бот, веб) и централизованно подключаются интеграции (БД, LLM, отправка уведомлений в Telegram). Бизнес-логика, данные и авторизация живут здесь; клиенты остаются тонкими.

Детальные итерации и DoD — в [plan.md](../plan.md). Специфичные по итерации списки: [tasklist-backend-iteration-2-core.md](tasklist-backend-iteration-2-core.md), [tasklist-backend-iteration-4-schedule-hw.md](tasklist-backend-iteration-4-schedule-hw.md), [tasklist-backend-iteration-6-progress.md](tasklist-backend-iteration-6-progress.md).

## Связь с plan.md

| Этап в plan.md | Роль для backend |
|----------------|------------------|
| [Итерация 2: Backend Core](../plan.md#итерация-2-backend-core) | FastAPI, PostgreSQL, доменная модель, базовые CRUD, основа API |
| [Итерация 3: Персонализированный диалог](../plan.md#итерация-3-персонализированный-диалог) | Контекст и LLM только через backend; бот переводится на вызовы API |
| [Итерация 4: Расписание и домашние задания](../plan.md#итерация-4-расписание-и-домашние-задания) | Полный цикл занятий и ДЗ через API, напоминания |
| [Итерация 6: Прогресс и аналитика](../plan.md#итерация-6-прогресс-и-аналитика) | Агрегация `Progress`, отчёты, данные для LLM-контекста |

Итерация 5 (веб) не входит в область backend-тасклиста напрямую; фронт потребляет стабилизированное API после итераций 2–4.

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

---

## Итерация 2 — Backend Core

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 01 | Выбор стека и фиксация архитектурных решений (ADR) | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-01-adr/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-01-adr/summary.md) |
| 02 | Инициализация пакета `backend/` и базовой конфигурации | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-02-init/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-02-init/summary.md) |
| 03 | Проектирование и документирование API-контрактов | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-03-api-contracts/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-03-api-contracts/summary.md) |
| 04 | Реализация CRUD API для доменных сущностей | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-04-crud-api/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-04-crud-api/summary.md) |
| 05 | PostgreSQL: ORM-модели и миграции | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-05-postgres-migrations/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-05-postgres-migrations/summary.md) |
| 06 | LLM-интеграция: клиент и формирование контекста | 📋 Planned | [план](impl/backend/iteration-2-core/tasks/task-06-llm-integration/plan.md) \| [summary](impl/backend/iteration-2-core/tasks/task-06-llm-integration/summary.md) |

---

### Задача 01: Выбор стека и фиксация архитектурных решений (ADR) 📋

#### Цель

Зафиксированы ключевые решения по фреймворку (ориентир — FastAPI), СУБД (PostgreSQL, см. [data-model.md](../data-model.md), [ADR-001](../adr/adr-001-database.md)), ORM/миграциям и границам пакета `backend/`.

#### Состав работ

- [ ] Согласовать стек с [vision.md](../vision.md)
- [ ] Оформить ADR при необходимости (новые решения помимо уже принятых)
- [ ] Зафиксировать структуру каталогов `backend/src/ttlg_backend/` (api, services, storage, llm)

#### Артефакты

- `docs/adr/` — записи решений при отклонениях от vision
- `backend/` — ориентир структуры репозитория из vision

#### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-01-adr/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-01-adr/summary.md)

---

### Задача 02: Инициализация пакета `backend/` и базовой конфигурации 📋

#### Цель

Каркас приложения запускается локально; зависимости через **uv**; настройки — **pydantic-settings** + `.env` / `.env.example`.

#### Состав работ

- [ ] Создать пакет `backend/`, точку входа приложения FastAPI
- [ ] Подключить конфиг (`DATABASE_URL`, LLM-параметры из [vision.md](../vision.md))
- [ ] Обновить `Makefile` / корневой `pyproject.toml` при необходимости

#### Артефакты

- `backend/src/ttlg_backend/`
- `.env.example` — без секретов
- `Makefile` — цели для установки и запуска backend

#### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-02-init/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-02-init/summary.md)

---

### Задача 03: Проектирование и документирование API-контрактов 📋

#### Цель

Описаны REST-контракты для сущностей из [data-model.md](../data-model.md) (`User`, `Lesson`, `Assignment`, `Progress`, `Dialogue`, `Message`): ресурсы, схемы запросов/ответов, коды ошибок (черновик согласуется с задачей 11).

#### Состав работ

- [ ] Свести эндпоинты к ресурсам домена
- [ ] Зафиксировать в OpenAPI (генерация из FastAPI) или кратком `docs/` при необходимости
- [ ] Учесть роли `student` / `teacher` на уровне проектирования

#### Артефакты

- OpenAPI-схема приложения (через FastAPI)
- При необходимости — `docs/api.md` или фрагменты в ADR

#### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-03-api-contracts/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-03-api-contracts/summary.md)

---

### Задача 04: Реализация CRUD API для доменных сущностей 📋

#### Цель

Базовые операции create/read/update/delete (или read/write по смыслу сущности) для всех перечисленных в [data-model.md](../data-model.md) сущностей; валидация входа (Pydantic), базовые проверки прав (минимум — заготовка под роли).

#### Состав работ

- [ ] Роутеры и зависимости FastAPI
- [ ] Вызовы сервисного слоя / репозиториев
- [ ] Smoke-проверки ключевых маршрутов

#### Артефакты

- `backend/src/ttlg_backend/api/`
- `backend/src/ttlg_backend/services/`

#### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-04-crud-api/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-04-crud-api/summary.md)

---

### Задача 05: PostgreSQL: ORM-модели и миграции 📋

#### Цель

Схема БД соответствует [data-model.md](../data-model.md); миграции применяются без ошибок; `DATABASE_URL` из конфига.

#### Состав работ

- [ ] Модели ORM и связи
- [ ] Цепочка миграций (инициализация + enum/поля как в модели)
- [ ] Документировать локальный запуск БД (например Docker Compose) при необходимости

#### Артефакты

- `backend/src/ttlg_backend/storage/` или аналог
- Файлы миграций в репозитории

#### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-05-postgres-migrations/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-05-postgres-migrations/summary.md)

---

### Задача 06: LLM-интеграция: клиент и формирование контекста 📋

#### Цель

Единая точка вызова **OpenRouter** (OpenAI-compatible) из backend по [integrations.md](../integrations.md): `base_url`, модель и ключ из конфига; заготовка сборки промпта (системная роль + контекст из БД + вопрос) без утечек секретов в логи.

#### Состав работ

- [ ] Клиент LLM с таймаутом и обработкой ошибок
- [ ] Сервис формирования контекста ученика (занятия, ДЗ — по мере наличия данных)
- [ ] Не логировать токены и избыточные персональные данные

#### Артефакты

- `backend/src/ttlg_backend/llm/` (или `services/llm.py` — по структуре репо)

#### Документы

- 📋 [План](impl/backend/iteration-2-core/tasks/task-06-llm-integration/plan.md)
- 📝 [Summary](impl/backend/iteration-2-core/tasks/task-06-llm-integration/summary.md)

---

## Итерация 3 — Персонализированный диалог (backend-аспект)

Связанный tasklist бота: [tasklist-bot-iteration-3-personalized-dialog.md](tasklist-bot-iteration-3-personalized-dialog.md).

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 07 | Готовность API для бота без прямого LLM: диалог, история, контекст | 📋 Planned | [план](impl/backend/iteration-3-personalized-dialog/tasks/task-07-dialog-api/plan.md) \| [summary](impl/backend/iteration-3-personalized-dialog/tasks/task-07-dialog-api/summary.md) |

---

### Задача 07: Готовность API для бота без прямого LLM: диалог, история, контекст 📋

#### Цель

Бот может полностью обходиться без прямых вызовов LLM: эндпоинт(ы) для отправки сообщения ученика, сохранения `Dialogue` / `Message`, получения ответа ассистента с обогащением контекста из БД (см. DoD итерации 3 в [plan.md](../plan.md)).

#### Состав работ

- [ ] API сценария «сообщение ученика → ответ ассистента» с персистентностью истории
- [ ] Включение в промпт данных ученика (расписание, ДЗ при наличии)
- [ ] Согласование контракта с рефакторингом бота (бот — тонкий клиент)

#### Артефакты

- Расширение `backend/src/ttlg_backend/api/` и сервисов диалога

#### Документы

- 📋 [План](impl/backend/iteration-3-personalized-dialog/tasks/task-07-dialog-api/plan.md)
- 📝 [Summary](impl/backend/iteration-3-personalized-dialog/tasks/task-07-dialog-api/summary.md)

> **Примечание:** сам рефакторинг кода бота на вызовы backend — в области bot; здесь — обеспечение и стабильность backend API для этого сценария.

---

## Итерация 4 — Расписание и домашние задания

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 08 | Расписание и ДЗ: полный цикл API + статусы | 📋 Planned | [план](impl/backend/iteration-4-schedule-hw/tasks/task-08-schedule-hw-api/plan.md) \| [summary](impl/backend/iteration-4-schedule-hw/tasks/task-08-schedule-hw-api/summary.md) |
| 09 | Напоминания через backend (Notifier → Telegram Bot API) | 📋 Planned | [план](impl/backend/iteration-4-schedule-hw/tasks/task-09-reminders-notifier/plan.md) \| [summary](impl/backend/iteration-4-schedule-hw/tasks/task-09-reminders-notifier/summary.md) |

---

### Задача 08: Расписание и ДЗ: полный цикл API + статусы 📋

#### Цель

Создание/обновление/завершение занятий; создание ДЗ; корректные переходы статусов `Assignment` (`pending` / `submitted` / `overdue`) по [data-model.md](../data-model.md) и DoD итерации 4 в [plan.md](../plan.md).

#### Состав работ

- [ ] Эндпоинты для жизненного цикла `Lesson` и `Assignment`
- [ ] Бизнес-правила смены статусов (в т.ч. просрочка при необходимости)
- [ ] Данные доступны для ответов бота («что задано?», «когда занятие?»)

#### Артефакты

- Расширение API и сервисов итерации 4

#### Документы

- 📋 [План](impl/backend/iteration-4-schedule-hw/tasks/task-08-schedule-hw-api/plan.md)
- 📝 [Summary](impl/backend/iteration-4-schedule-hw/tasks/task-08-schedule-hw-api/summary.md)

---

### Задача 09: Напоминания через backend (Notifier → Telegram Bot API) 📋

#### Цель

Триггеры напоминаний о занятиях и ДЗ инициируются из backend; доставка — через [Telegram Bot API](https://core.telegram.org/bots/api) согласно [integrations.md](../integrations.md) (клиенты не шлют напрямую в LLM; исходящие уведомления — через единый слой Notifier в ядре).

#### Состав работ

- [ ] Механизм планирования/очереди или периодические задачи (минимально достаточный вариант)
- [ ] Вызов `sendMessage` (или аналог) с учётом `telegram_id` пользователя
- [ ] Устойчивость к сбоям Telegram (таймаут, логирование без токенов)

#### Артефакты

- Модуль уведомлений в `backend/src/ttlg_backend/` (например `services/notifier.py`)

#### Документы

- 📋 [План](impl/backend/iteration-4-schedule-hw/tasks/task-09-reminders-notifier/plan.md)
- 📝 [Summary](impl/backend/iteration-4-schedule-hw/tasks/task-09-reminders-notifier/summary.md)

---

## Итерация 6 — Прогресс и аналитика

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 10 | Прогресс: агрегация за период и отчёты | 📋 Planned | [план](impl/backend/iteration-6-progress/tasks/task-10-progress-analytics/plan.md) \| [summary](impl/backend/iteration-6-progress/tasks/task-10-progress-analytics/summary.md) |

---

### Задача 10: Прогресс: агрегация за период и отчёты 📋

#### Цель

Автоматический или инициируемый расчёт `Progress` за период; API для сводок по ученику и учителю; данные прогресса могут подмешиваться в LLM-контекст (см. DoD итерации 6 в [plan.md](../plan.md)).

#### Состав работ

- [ ] Агрегация по занятиям и ДЗ за `period_start` / `period_end`
- [ ] Эндпоинты отчётов (ученик / преподаватель)
- [ ] Интеграция с сервисом формирования промпта при необходимости

#### Артефакты

- Сервисы и API раздела прогресса

#### Документы

- 📋 [План](impl/backend/iteration-6-progress/tasks/task-10-progress-analytics/plan.md)
- 📝 [Summary](impl/backend/iteration-6-progress/tasks/task-10-progress-analytics/summary.md)

---

## Cross-итерационные задачи

### Список задач

| Задача | Описание | Статус | Документы |
|--------|----------|--------|-----------|
| 11 | Конвенции API: форматы запросов, коды ошибок, версионирование | 📋 Planned | [план](impl/backend/cross/task-11-api-conventions/plan.md) \| [summary](impl/backend/cross/task-11-api-conventions/summary.md) |
| 12 | Актуализация документации и сценарии локального запуска всей системы | 📋 Planned | [план](impl/backend/cross/task-12-docs-and-run/plan.md) \| [summary](impl/backend/cross/task-12-docs-and-run/summary.md) |

---

### Задача 11: Конвенции API: форматы запросов, коды ошибок, версионирование 📋

#### Цель

Единые правила для клиентов: структура тел ошибок, HTTP-коды, идемпотентность где нужно; политика версионирования API (префикс `/v1` или аналог); описание зафиксировано в `docs/` и соблюдается в реализации.

#### Состав работ

- [ ] Зафиксировать формат ошибок и коды в документе или ADR
- [ ] Согласовать префикс версии и правила breaking changes
- [ ] Применить единый обработчик исключений FastAPI

#### Артефакты

- Фрагмент в `docs/` (например раздел в `integrations.md` или отдельный `docs/api-conventions.md`)

#### Документы

- 📋 [План](impl/backend/cross/task-11-api-conventions/plan.md)
- 📝 [Summary](impl/backend/cross/task-11-api-conventions/summary.md)

---

### Задача 12: Актуализация документации и сценарии локального запуска всей системы 📋

#### Цель

[vision.md](../vision.md), [data-model.md](../data-model.md), [integrations.md](../integrations.md) отражают фактическую реализацию; в README / Makefile описан запуск bot + backend + БД одной командой или краткой последовательностью.

#### Состав работ

- [ ] Синхронизировать документацию с реализованными эндпоинтами и схемой
- [ ] Описать переменные окружения и порядок `make` / `uv`
- [ ] При необходимости обновить [plan.md](../plan.md) только статусами/ссылками, без расширения scope

#### Артефакты

- `README.md`, `docs/*.md`, `Makefile`

#### Документы

- 📋 [План](impl/backend/cross/task-12-docs-and-run/plan.md)
- 📝 [Summary](impl/backend/cross/task-12-docs-and-run/summary.md)

---

## Качество и инженерные практики

- **Тесты:** smoke на критичных эндпоинтах; по мере роста — unit-тесты сервисов и репозиториев.
- **Линтинг и форматирование:** Ruff (или согласованный в Makefile инструмент), цели в Makefile.
- **Наблюдаемость:** стандартный `logging` с именем модуля; внешние вызовы (LLM, Telegram) — таймауты, обработка ошибок, в логах без токенов и лишних персональных данных.
- **Контракты API:** обратно совместимые изменения без смены версии; ломающие — новая версия маршрута или явное решение в ADR; клиенты бота и веб опираются на одни соглашения (задача 11).
