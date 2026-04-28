# Ревью Docker-конфигурации (итерация «локальный полный стек»)

**Дата:** 2026-04-27  
**Основа:** чеклист skill *docker-expert* (multi-stage, security, compose, healthchecks, контекст сборки).

## Проверенные пункты

| Область | Результат |
|---------|-----------|
| Multi-stage Dockerfile (backend, bot, frontend) | Да: builder → runtime, в финале только нужные артефакты |
| Порядок слоёв / кэш зависимостей | Да: lock + pyproject / package.json до копирования исходников |
| `.dockerignore` | Да: отдельно на сервис, сокращение контекста |
| Non-root в runtime | Да: UID/GID 1001 (Python), `nodejs` (frontend) |
| Секреты не в образе | Да: нет `COPY .env`; runtime через `env_file` / `environment` в Compose |
| Healthcheck | Да: backend и frontend; у бота HTTP нет — healthcheck не задан (ожидаемо) |
| Зависимости Compose | Да: `depends_on` + `condition: service_healthy` для db/backend |
| Сеть БД | `db_net` с `internal: true`; backend на `db_net` + `edge`; bot/frontend только на `edge` (нужен выход в интернет для Telegram и LLM) |
| Alembic в образе backend | Да: `backend/alembic` + `alembic.ini` для `make stack-migrate` |

## Отклонения и компромиссы

1. **Next.js standalone в monorepo:** каталог `.next/standalone/` нельзя «сплющивать» в один `/app`: у pnpm в `node_modules` относительные symlink’и (например `next` → `../../node_modules/.pnpm/...`), они валидны только при структуре **`/app/node_modules` + `/app/frontend/server.js`** и запуске с **`WORKDIR /app/frontend`**.
2. **Порт PostgreSQL на хост (`5432:5432`)** сохранён для обратной совместимости с `make backend-db-migrate` на хосте и `.env` с `127.0.0.1`. Полная изоляция БД без публикации порта — отдельный профиль/override при необходимости.
3. **`make stack-health`** — `scripts/stack_health.py`: HTTP к backend `/health` и frontend `:3000`, затем `docker compose ps` по сервисам `db`, `backend`, `bot`, `frontend` (бот без своего HTTP — только `State` в compose).
4. **Образы на базе Debian slim / Alpine** — периодически обновлять теги и прогонять сканер уязвимостей (не входило в объём итерации).

## Уточнение после прогона

- **Корневой `.dockerignore` обязателен** при `build.context: .`: иначе в демон уезжает весь репо включая `frontend/node_modules` / `.next`, сборка долгая и может завершиться `rpc error … EOF` (демон/ресурсы), без явной ошибки «no space».
- **Один lockfile для frontend:** зависимости задаются в `frontend/package.json`, но **`pnpm-lock.yaml` только в корне репозитория** (workspace). Старый `frontend/pnpm-lock.yaml` удалён — после правок зависимостей выполняйте `pnpm install` из **корня** репо.

## Ручной продуктовый смоук

**Дата:** 2026-04-27. Владелец репозитория подтвердил прохождение смоука на **полном стеке в Docker** (Compose): доступность API и веб-клиента, продуктовые сценарии в связке с ботом при валидных секретах в `.env`. Порядок команд и переменные — [how-to-docker.md](../how-to-docker.md).

## Бэклог (некритично)

- Лимиты CPU/RAM в Compose для локальной стабильности.
- Профиль `db-only` при росте числа сервисов.
- Отдельный workflow публикации в GHCR — следующая итерация tasklist-devops.
