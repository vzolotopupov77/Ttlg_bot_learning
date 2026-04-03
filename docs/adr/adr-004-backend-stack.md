# ADR-004: Backend-стек (FastAPI, uvicorn, asyncpg, pydantic-settings, openai SDK)

| | |
|---|---|
| **Статус** | Принято |
| **Дата** | 2026-04-01 |
| **Контекст** | Выбор компонентов HTTP-слоя backend, драйвера БД, конфигурации и LLM-клиента для проекта TTLG. СУБД задана в [ADR-001](adr-001-database.md); ORM, миграции и тестовый стек — в [ADR-002](adr-002-orm-migrations-tests.md). |

---

## Контекст

Backend — ядро системы: принимает HTTP-запросы от Telegram-бота и веб-клиента, обращается к PostgreSQL через SQLAlchemy async и вызывает LLM-провайдер (OpenRouter). Нужно выбрать:

1. **Веб-фреймворк** — обрабатывает HTTP, валидирует схемы, генерирует OpenAPI.
2. **ASGI-сервер** — запускает приложение в prod и dev.
3. **Драйвер PostgreSQL** — async-соединение с БД.
4. **Конфигурация** — загрузка настроек и секретов из окружения.
5. **LLM-клиент** — вызов OpenRouter через OpenAI-compatible API.

---

## Рассмотренные варианты

### 1. Веб-фреймворк

#### FastAPI ✅ — выбрано

**Плюсы:**
- Нативная async-поддержка (`async def` роутеры, `Depends`-инъекции).
- Автоматическая генерация OpenAPI/Swagger из аннотаций Pydantic — без отдельного кода.
- Де-факто стандарт в Python async backend 2023–2026; огромная документация и community.
- Тонкая обёртка над Starlette — легко встраивать middleware, lifespan, фоновые задачи.

**Минусы:**
- Pydantic v2 порой требует явных аннотаций там, где Pydantic v1 был терпимее.

**Вывод:** оптимальный выбор для async HTTP API с OpenAPI из коробки.

#### Litestar

**Плюсы:** строгая типизация, быстрее FastAPI в ряде бенчмарков.

**Минусы:** меньше примеров и готовых интеграций; команда меньше знакома с экосистемой.

**Вывод:** интересный кандидат на будущее; сейчас не даёт преимуществ над FastAPI.

#### Flask + flask-pydantic / Quart

**Плюсы:** знакомы большинству Python-разработчиков.

**Минусы:** sync-ориентирован (Quart добавляет async, но с накладными расходами); OpenAPI — дополнительные пакеты; интеграция с SQLAlchemy async сложнее.

**Вывод:** избыточная сложность для async-стека.

#### Django (+ Django REST Framework)

**Плюсы:** «батарейки включены»; Admin, ORM, auth из коробки.

**Минусы:** монолитная архитектура; Django ORM не подходит, т.к. выбран SQLAlchemy ([ADR-002](adr-002-orm-migrations-tests.md)); async-экосистема DRF отстаёт.

**Вывод:** не рассматривается.

---

### 2. ASGI-сервер

#### uvicorn ✅ — выбрано

**Плюсы:**
- Рекомендован самой командой FastAPI и Starlette.
- `uvicorn[standard]` включает `uvloop` (ускоритель event loop) и `websockets`.
- `--reload` для dev без лишних зависимостей.

**Минусы:** для high-load prod обычно ставят Gunicorn как process manager поверх uvicorn (`gunicorn -k uvicorn.workers.UvicornWorker`); для MVP это излишество.

**Вывод:** единственный рассматривавшийся вариант; при масштабировании — добавить Gunicorn без смены кода.

---

### 3. Async-драйвер PostgreSQL

#### asyncpg ✅ — выбрано

**Плюсы:**
- Нативный async-протокол PostgreSQL (бинарный); самый быстрый Python-драйвер.
- Первоклассная поддержка в SQLAlchemy async (`postgresql+asyncpg://`).
- Уже задан в [ADR-001](adr-001-database.md) как следствие выбора PostgreSQL.

**Минусы:** только для PostgreSQL; не подходит для SQLite (для тестов используется `aiosqlite`).

**Вывод:** решение уже зафиксировано в ADR-001, здесь подтверждается.

---

### 4. Конфигурация и секреты

#### pydantic-settings ✅ — выбрано

**Плюсы:**
- Единый класс `BaseSettings` читает переменные из окружения и `.env` с валидацией типов.
- `SecretStr` — секреты не утекают в repr/логи.
- Согласован с Pydantic v2 (уже используется в FastAPI-роутерах).
- Поддержка `field_validator` и `model_validator` — сложная валидация конфига без внешних зависимостей.

**Минусы:** ещё одна зависимость (незначительно — Pydantic уже есть через FastAPI).

**Вывод:** лучший выбор в стеке FastAPI + Pydantic.

#### dynaconf

**Плюсы:** поддержка нескольких форматов (TOML, YAML, env); layered environments.

**Минусы:** нет нативной интеграции с Pydantic; лишняя зависимость без выгоды.

**Вывод:** отклонено.

#### python-dotenv напрямую

**Плюсы:** минимализм.

**Минусы:** нет валидации типов; секреты в обычных строках.

**Вывод:** недостаточно безопасно и удобно.

---

### 5. LLM-клиент (OpenRouter)

#### openai SDK ✅ — выбрано

**Плюсы:**
- OpenRouter полностью совместим с OpenAI API (`base_url` меняется, ключ и методы — те же).
- `AsyncOpenAI` — нативный async; встроенная поддержка таймаутов, retry, streaming.
- `timeout` в конструкторе — не нужен дополнительный `httpx.AsyncClient` для LLM.

**Минусы:** тянет зависимость openai (~4 МБ); при смене провайдера на несовместимый API потребуется замена клиента.

**Вывод:** оптимально, пока провайдер OpenAI-compatible (OpenRouter, Azure OpenAI и т.п.).

#### httpx напрямую

**Плюсы:** нет лишних зависимостей; полный контроль.

**Минусы:** ручная реализация retry, streaming, маппинга ошибок; дублирование того, что уже есть в openai SDK.

**Вывод:** избыточно при наличии совместимого SDK.

#### LangChain / LlamaIndex

**Плюсы:** абстракции для chains, RAG, memory.

**Минусы:** тяжёлые зависимости; избыточные абстракции для текущего MVP (один вызов LLM).

**Вывод:** не вводим; вернуться при появлении RAG-сценариев.

---

## Решение

| Компонент | Выбор | Пакет |
|---|---|---|
| Веб-фреймворк | **FastAPI** | `fastapi` |
| ASGI-сервер | **uvicorn** | `uvicorn[standard]` |
| Драйвер PostgreSQL | **asyncpg** | `asyncpg` |
| Конфигурация | **pydantic-settings** | `pydantic-settings` |
| LLM-клиент | **openai SDK** (async) | `openai` |

Все пять компонентов — в `[project.dependencies]` пакета `ttlg-backend`.

---

## Последствия

- Пакет `ttlg-backend` зависит от FastAPI; бот (`ttlg-bot`) обращается к backend только через HTTP — не знает о FastAPI.
- При введении Gunicorn в prod — добавить `gunicorn` в зависимости; конфиг dev (`--reload`) и prod (`-k UvicornWorker`) разделить через Makefile / Docker entrypoint.
- Смена LLM-провайдера на OpenAI-compatible: только переменная `OPENROUTER_BASE_URL` и `LLM_MODEL` — код не меняется.
- Смена на несовместимый провайдер: изолировать за интерфейсом `LLMClient`; замена только `backend/src/ttlg_backend/llm/client.py`.
- Тайпчекер (ty или mypy) — при введении потребует аннотаций в `Settings`-классах; существующие `SecretStr`, `field_validator` с аннотациями уже совместимы.
