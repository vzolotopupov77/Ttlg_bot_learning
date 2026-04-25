# Онбординг: с чего начать новому участнику

Полный набор **системных требований** и **переменных окружения** — в [README.md](../README.md) и [.env.example](../.env.example). Ниже — пошаговый маршрут.

---

## 1. Клонирование и первичная настройка

1. Склонируйте репозиторий.
2. Установите: **Python 3.12**, **uv** (0.5+), **Docker**, **Node.js 20 LTS**, **pnpm** (9+). Таблица и ссылки — [README.md § Системные требования](../README.md#системные-требования).
3. **Windows:** команды `make` выполняйте в **Git Bash** или **WSL**; в PowerShell смотрите раскрытие в [Makefile](../Makefile).
4. Скопируйте окружение:
   - `cp .env.example .env` — в корне (бот + backend).
   - `cp frontend/.env.local.example frontend/.env.local` — фронт (см. комментарии в файле).
5. Установите зависимости:
   - `uv sync --all-packages` (или `make install`).
   - `pnpm install` в корне репозитория (workspace, пакет `frontend`).

---

## 2. Настройка каждого компонента

### PostgreSQL (общая БД)

```bash
make backend-db-up
```

Контейнер слушает `localhost:5432` (см. [docker-compose.yml](../docker-compose.yml)). В `.env` задайте `DATABASE_URL` как в `.env.example`.

```bash
make backend-db-migrate
make backend-db-seed
```

### Backend (FastAPI)

- В `.env`: как минимум `SECRET_KEY`, `DATABASE_URL`; для реальных ответов LLM — `OPENROUTER_API_KEY` (и при необходимости учётные данные сида/преподавателя).
- Запуск: `make backend-run` → по умолчанию **http://127.0.0.1:8000**  
  Подробнее: [backend/README.md](../backend/README.md).

### Telegram-бот

- Код: **`src/ttlg_bot/`** (каталог `bot/` в корне пустой).
- В `.env`: `TELEGRAM_BOT_TOKEN`, `BACKEND_URL` (тот же хост, что и API).
- Запускайте **после** backend: `make run` (long polling).
- Для ручного E2E зарегистрируйте пользователя с вашим `telegram_id` — [integrations.md](integrations.md).

### Frontend (Next.js)

- `frontend/.env.local`: `NEXT_PUBLIC_API_URL`, `AUTH_SECRET` и прочее по примеру.
- Запуск: `make frontend-dev` (или `pnpm --filter frontend dev`).  
  Подробнее: [frontend/README.md](../frontend/README.md).

### Тестовая база для backend-тестов (однократно)

При запущенном Docker с PostgreSQL:

```bash
make backend-db-test-create
```

`DATABASE_TEST_URL` в `.env` должен указывать на `ttlg_test` (см. `.env.example`).

---

## 3. Проверка, что всё работает

| Что | Команда / действие | Признак успеха |
|-----|--------------------|----------------|
| API жив | `curl -s http://127.0.0.1:8000/health` | JSON: `"status":"ok"` (при рабочей БД) или читаемый ответ без ошибки сети |
| Документация API | Откройте в браузере `http://127.0.0.1:8000/docs` | Загружается Swagger UI |
| Backend-тесты | `make backend-test` (нужен PostgreSQL + `ttlg_test`) | `pytest` завершается с **0 failures** |
| Тесты бота | `make bot-test` | `pytest` в `tests/` — **passed** (SQLite in-memory, Docker не обязателен) |
| Линт Python | `make lint` | Без отчёта об ошибках |
| Линт фронта | `make frontend-lint` | ESLint завершается без ошибок |
| Фронт-тесты (отдельно) | `make frontend-test` | Vitest: все тесты зелёные (не входят в `make check`, см. Makefile) |
| Полный барьер как в CI | `make check` = lint + `backend-test` + `bot-test` + `frontend-lint` | Все этапы успешны |

> Для `backend-test` должен быть доступен `DATABASE_TEST_URL` (PostgreSQL, база `ttlg_test`).

---

## 4. С чего смотреть код (точки входа)

| Область | Старт |
|---------|--------|
| Архитектура целиком | [architecture.md](architecture.md), [vision.md](vision.md) |
| Backend приложение | `backend/src/ttlg_backend/main.py` |
| API и зависимости | `backend/src/ttlg_backend/api/` |
| Модели БД | `backend/src/ttlg_backend/storage/models.py` |
| Бот | `src/ttlg_bot/bot.py`, `src/ttlg_bot/services/backend_client.py` |
| Веб: маршруты App Router | `frontend/src/app/` |
| Сессия/редиректы | `frontend/middleware.ts` (см. комментарии в [page.tsx](../frontend/src/app/page.tsx)) |
| Контракты HTTP | [tech/api-contracts.md](tech/api-contracts.md) |
| OpenAPI (артефакт) | [openapi.json](openapi.json), генерация: `make openapi-export` |

---

## 5. Рабочий процесс (итерации, план, summary)

- **Продуктовая дорожная карта:** [plan.md](plan.md).
- **Декомпозиция по областям:** [tasks/tasklist-backend.md](tasks/tasklist-backend.md), [tasks/tasklist-frontend.md](tasks/tasklist-frontend.md), [tasks/tasklist-database.md](tasks/tasklist-database.md) и др.
- **Итерации с артефактами `plan` / `summary`:** встречаются внутри [tasks/impl/](tasks/impl/) (пример структуры: подпапка итерации + файлы `plan.md` / `summary.md` у отдельных задач).
- **Правила согласования** для агентов/IDE: [.cursor/rules/workflow.mdc](../.cursor/rules/workflow.mdc) — фазы Plan, два явных согласования перед реализацией и перед фиксацией.

---

## 6. Как готовить изменения (проверки качества)

1. Перед PR локально: **`make check`** (Ruff, pytest backend+бот, ESLint фронта).
2. Дополнительно при работе с UI/логике фронта: **`make frontend-test`**, **`make frontend-build`**.
3. **Формат Python:** `make format` (Ruff).
4. Не коммитьте `.env` с секретами; `docs/openapi.json` обновляйте при изменении контракта: `make openapi-export`. Рекомендации по PR: [contributing.md](contributing.md).
