# Локальный запуск полного стека в Docker

Краткий гайд: PostgreSQL + FastAPI backend + Telegram-бот + Next.js frontend одной командой Compose. Обоснование структуры образов — [ADR-005](adr/adr-005-devops-artifacts-layout.md).

## Предусловия

- Docker **24+**, Compose **v2**
- В корне репозитория: `cp .env.example .env` и заполните переменные (см. ниже)
- Make: удобно из **Git Bash** или WSL на Windows ([README.md](../README.md) § системные требования)

## Обязательные переменные для полного стека

Файл **`.env` в корне** репозитория используют и Compose-сервисы, и локальные `make`-команды.

| Переменная | Назначение |
|------------|------------|
| `SECRET_KEY` | Подпись JWT в backend |
| `AUTH_SECRET` | Тот же секрет для проверки JWT в Next.js middleware — **должен совпадать с `SECRET_KEY`** |
| `DATABASE_URL` | Для процессов на **хосте** оставьте `...@127.0.0.1:5432/...`. В контейнере backend Compose **переопределяет** URL на `db:5432` |
| `TELEGRAM_BOT_TOKEN` | Токен бота (валидный формат; иначе бот упадёт при старте) |
| `OPENROUTER_API_KEY` | Для реальных ответов LLM через backend |

`BACKEND_URL` в `.env` может указывать на `http://127.0.0.1:8000` — для сервиса **bot** Compose задаёт **`http://backend:8000`**.

Frontend в браузере ходит на **`http://localhost:8000`** (проброшенный порт backend). При сборке образа frontend задаётся `NEXT_PUBLIC_API_URL=http://localhost:8000`. Внутри контейнера Next для Server Components использует **`API_INTERNAL_URL=http://backend:8000`** (уже в `docker-compose.yml`).

## Порядок запуска

```bash
# 1. Сборка образов (опционально отдельно)
make stack-build

# 2. Поднять все сервисы
make stack-up

# 3. Миграции БД (одноразовый контейнер backend, сеть к PostgreSQL)
make stack-migrate

# 4. (По желанию) сид данных — пока только с хоста, с DATABASE_URL на localhost:
make backend-db-seed
```

Проверки:

- Стек: `make stack-health` (backend `/health`, корень frontend `:3000`, статусы контейнеров) или вручную `http://127.0.0.1:8000/health` и `http://localhost:3000`
- Frontend: `http://localhost:3000`
- Логи: `make stack-logs` или `make stack-logs-backend` (и другие имена сервисов из `docker compose ps`)

Остановка:

```bash
make stack-down
```

## Эквиваленты без Make

```bash
docker compose build
docker compose up -d --build
docker compose run --rm backend alembic -c backend/alembic.ini upgrade head
docker compose logs -f
docker compose down
```

## Отличия от запуска без Docker

| Без Docker | Docker |
|------------|--------|
| `make backend-db-up` только БД | `make stack-up` — БД + backend + bot + frontend |
| `make backend-run`, `make frontend-dev`, `make run` в разных терминалах | Один Compose; hot-reload в образах **не** настроен (production-сборки) |
| `frontend/.env.local` для Next | Для стека достаточно корневого `.env` с `AUTH_SECRET` и публичными URL при необходимости |

Подробнее про пошаговый режим без контейнеров приложений: [onboarding.md](onboarding.md).

## Типичные проблемы

| Симптом | Что проверить |
|---------|----------------|
| Порт **8000** или **3000** занят | Остановите другой процесс или измените проброс портов в `docker-compose.yml` |
| Backend **503** на `/health`, degraded | БД не готова; дождитесь healthy у `db`, выполните `make stack-migrate` |
| Frontend: ошибка логина / сессии | `AUTH_SECRET` в корневом `.env` и совпадение с `SECRET_KEY` backend |
| Бот падает в логах | Валидный `TELEGRAM_BOT_TOKEN`, доступ в интернет (Telegram API) |
| `stack-health` падает | Backend не слушает :8000 или не поднят; проверьте `http://127.0.0.1:8000/health` в браузере; нужен `python` в PATH |

## Ручная проверка зафиксировано

**Дата:** 2026-04-27.

| Проверка | Результат |
|----------|-----------|
| Сборка образов (`make stack-build` / `docker compose build`) | OK (после корневого `.dockerignore`, синхронизации `pnpm-lock.yaml` с workspace, правки runtime frontend под monorepo standalone) |
| Запуск стека (`make stack-up`), `db` / `backend` healthy | OK |
| Миграции (`make stack-migrate`) | OK |
| Backend `GET /health`, frontend `http://localhost:3000` | OK |
| Продуктовый смоук (сценарии UI / бот / API в связке со стеком в Docker) | OK (подтверждено владельцем репозитория) |

Детали ревью конфигурации и известные компромиссы: [tech/docker-review-notes.md](tech/docker-review-notes.md).

## Запуск с образами из GHCR (без локальной сборки)

GitHub Actions пайплайн (`.github/workflows/docker-publish.yml`) собирает образы при push в `main` или при теге `v*.*.*` и публикует их в GitHub Container Registry:

| Образ | GHCR |
|-------|------|
| backend | `ghcr.io/vzolotopupov77/ttlg-backend` |
| bot | `ghcr.io/vzolotopupov77/ttlg-bot` |
| frontend | `ghcr.io/vzolotopupov77/ttlg-frontend` |

Теги: `latest` (из `main`), `sha-<короткий>` (каждый push), `<version>` / `<major>.<minor>` (из тегов `v*.*.*`).

### Логин в GHCR (если образы приватные)

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u <github-user> --password-stdin
```

### Порядок запуска с registry-образами

```bash
# 1. Скачать образы
docker compose -f docker-compose.yml -f docker-compose.ghcr.yml pull

# 2. Поднять стек (без локальной сборки)
docker compose -f docker-compose.yml -f docker-compose.ghcr.yml up -d

# 3. Миграции
docker compose -f docker-compose.yml -f docker-compose.ghcr.yml run --rm backend alembic -c backend/alembic.ini upgrade head
```

Для конкретного тега замените `latest`:

```bash
GHCR_TAG=v1.2.3 docker compose -f docker-compose.yml -f docker-compose.ghcr.yml pull
GHCR_TAG=v1.2.3 docker compose -f docker-compose.yml -f docker-compose.ghcr.yml up -d
```

> После выхода пайплайна образы видны в разделе **Packages** репозитория на GitHub.
> Override-файл: [`docker-compose.ghcr.yml`](../docker-compose.ghcr.yml).

## Дополнительно

- Каталог Dockerfile: [devops/README.md](../devops/README.md)
- Список задач DevOps: [tasks/tasklist-devops.md](tasks/tasklist-devops.md)
- Пайплайн GHCR: [`.github/workflows/docker-publish.yml`](../.github/workflows/docker-publish.yml)
