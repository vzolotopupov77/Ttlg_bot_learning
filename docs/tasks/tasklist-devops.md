# DevOps Tasklist (локальный стек, контейнеры, GHCR)

## Обзор

**Цель** — подготовительная итерация DevOps: единая структура артефактов, **локальный запуск полного стека** (PostgreSQL, backend, бот, frontend) через Docker, удобные команды `Makefile` и документация. **Полноценный CI/CD** (тесты в пайплайне, деплой, матрица версий) — **следующие итерации**; здесь — фундамент: образы, compose, **публикация образов в GitHub Container Registry (GHCR)** через GitHub Actions.

**Связь с репо:** бот `src/ttlg_bot/`, backend `backend/`, веб `frontend/`; корневой `docker-compose.yml` — полный стек (db + backend + bot + frontend). Продуктовая дорожная карта: [plan.md](../plan.md).

**Актуализация:** 2026-04-27 — итерация 1 (локальный полный стек) выполнена и **подтверждена ручным продуктовым смоуком** (см. [how-to-docker.md — раздел «Ручная проверка зафиксировано»](../how-to-docker.md#ручная-проверка-зафиксировано)); итерация 2 (GHCR/GHA) — 🚧 реализована, ожидает ручного подтверждения (push в main и проверка pull).

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

## Итерации

| Итерация | Содержание |
|----------|------------|
| 1 | Локальный полный стек: `devops/`, Dockerfile'ы, корневой `docker-compose.yml`, `Makefile`, ревью, how-to, обновление документации |
| 2 | GitHub Actions: сборка и push в GHCR; compose с образами из registry; ручная проверка на образах из GHCR |

## Результаты итерации 1 (локальный полный стек, закрыта)

**Дата приёмки:** 2026-04-27.

| Что сделано | Где |
|-------------|-----|
| Структура образов и обоснование | [ADR-005](../adr/adr-005-devops-artifacts-layout.md), [devops/README.md](../../devops/README.md), `devops/{backend,bot,frontend}/` |
| Полный стек в Compose | Корневой [`docker-compose.yml`](../../docker-compose.yml), корневой [`.dockerignore`](../../.dockerignore) при `build.context: .` |
| Команды стека | [`Makefile`](../../Makefile): `stack-build`, `stack-up`, `stack-down`, `stack-ps`, `stack-logs`, `stack-health`, `stack-migrate`, `help` |
| Ревью и заметки | [docker-review-notes.md](../tech/docker-review-notes.md) |
| Инструкция по запуску | [how-to-docker.md](../how-to-docker.md) |

**Ручная приёмка:** сборка образов, подъём стека, миграции, `GET /health`, веб UI, продуктовый смоук — таблица в [how-to-docker — «Ручная проверка зафиксировано»](../how-to-docker.md#ручная-проверка-зафиксировано); краткое подтверждение — [docker-review-notes — «Ручной продуктовый смоук»](../tech/docker-review-notes.md#ручной-продуктовый-смоук).

**Дальше:** итерация 2 — задачи **08–10** (GHA → GHCR, compose с `image:`, проверка pull без локального build).

## Список задач

### Итерация 1 — локальный полный стек

| № | Описание | Статус | Документы / примечание |
|---|----------|--------|-------------------------|
| 01 | Структура `devops/` и обоснование (ADR) | ✅ | [ADR-005](../adr/adr-005-devops-artifacts-layout.md), [devops/README.md](../../devops/README.md) |
| 02 | Dockerfile и `.dockerignore` (backend, bot, frontend) | ✅ | `devops/*/` |
| 03 | Корневой `docker-compose.yml` — полный стек | ✅ | корень репо |
| 04 | `Makefile`: stack-up/down, status, logs, health, help | ✅ | `Makefile` (`stack-migrate` добавлен для Alembic в контейнере) |
| 05 | Ревью docker-конфигурации (skill **docker-expert**) | ✅ | [docker-review-notes.md](../tech/docker-review-notes.md) |
| 06 | Инструкция: локальный запуск через Docker Compose | ✅ | [how-to-docker.md](../how-to-docker.md) |
| 07 | Обновление проектной документации | ✅ | README, plan, architecture, doc-audit |

**Ручная приёмка итерации 1 (2026-04-27):** полный стек в Docker, миграции, `/health`, UI и продуктовый смоук — зафиксировано в [how-to-docker.md](../how-to-docker.md#ручная-проверка-зафиксировано) и [docker-review-notes.md](../tech/docker-review-notes.md#ручной-продуктовый-смоук).

### Итерация 2 — GHA, GHCR, запуск с registry

| № | Описание | Статус | Документы / примечание |
|---|----------|--------|-------------------------|
| 08 | GHA: сборка и публикация в GHCR | 🚧 | [`.github/workflows/docker-publish.yml`](../../.github/workflows/docker-publish.yml) |
| 09 | Ревью compose для облачных образов (image из registry) | 🚧 | [`docker-compose.ghcr.yml`](../../docker-compose.ghcr.yml), [how-to-docker.md § GHCR](../how-to-docker.md#запуск-с-образами-из-ghcr-без-локальной-сборки) |
| 10 | Проверка: полный стек на образах из GHCR локально | 📋 | После push в main и появления пакетов в GitHub Packages |

---

## Детализация задач

### Итерация 1: локальный полный стек

#### Задача 01: Структура `devops/` и ADR (ит. 1) ✅

##### Цель

Зафиксировать единую базовую директорию **devops/** и вложенность **по сервисам** (backend, bot, frontend) для Dockerfile, `.dockerignore` и будущих скриптов/конфигов CI без засорения корня репозитория.

##### Состав работ

- Подготовить схему каталогов: `devops/backend/`, `devops/bot/`, `devops/frontend/` (и при необходимости `devops/README.md` с однострочным назначением).
- Описать **обоснование** в **ADR** (кратко: почему не только корневые `Dockerfile`, почему разбивка по сервисам, совместимость с GHA `context` и `docker build`).
- Согласовать пути `build: context` / `dockerfile` в будущем compose с выбранной структурой.

##### Артефакты

- `devops/README.md` (опционально, но рекомендуется)
- `docs/adr/adr-005-devops-artifacts-layout.md` (следующий номер: в репо есть [adr-001..004](../adr/))

##### Definition of Done

**Agent self-check**

- [ ] ADR ссылается на реальные пути; номер ADR не конфликтует с существующими.
- [ ] В ADR явно: база `devops/`, подкаталоги per-service.

**User check**

- [ ] По прочтению ADR и `devops/README` (если есть) понятно, куда класть новый Dockerfile при добавлении сервиса.

---

#### Задача 02: Dockerfile и `.dockerignore` для backend, bot, frontend (ит. 1) ✅

##### Цель

Собираемые образы для **трёх** компонентов: FastAPI (uv), Telegram-бот (uv), Next.js (pnpm production build или согласованный multistage), с минимальным контекстом благодаря `.dockerignore`.

##### Состав работ

- **Backend:** production-запуск (например `uvicorn`), зависимости через **uv** workspace / пакет `ttlg-backend` в соответствии с [pyproject.toml](../../pyproject.toml); не копировать лишнее (тесты по политике в ADR/Dockerfile).
- **Bot:** `python -m ttlg_bot` (или эквивалент из репо); переменные окружения — через `env_file` / `environment` в compose, не секреты в образе.
- **Frontend:** `pnpm` filter `frontend`, `next build` + `next start` (или образ под standalone output — согласовать с `frontend/next.config.*`).
- Для каждого сервиса — **`.dockerignore`** (node_modules, .next, venv, __pycache__, .git, coverage и т.д.).

##### Артефакты

- `devops/backend/Dockerfile`, `devops/backend/.dockerignore`
- `devops/bot/Dockerfile`, `devops/bot/.dockerignore`
- `devops/frontend/Dockerfile`, `devops/frontend/.dockerignore`

##### Definition of Done

**Agent self-check**

- [ ] `docker build` для каждого из трёх контекстов завершается без ошибки (на машине с Docker).
- [ ] Нет копирования `.env` с секретами в слои образа.

**User check**

- [ ] Командами из инструкции (после задачи 06) образы пересобираются предсказуемо; размер контекстов не «тянет» весь диск.

---

#### Задача 03: Единый корневой `docker-compose.yml` (полный стек) (ит. 1) ✅

##### Цель

Один файл **[docker-compose.yml](../../docker-compose.yml)** с сервисами **db + backend + bot + frontend**, сетью, зависимостями `depends_on` (и healthcheck для db), **без** отдельного устаревшего compose «только БД», кроме случая явной необходимости (тогда — документированный override, не дублирование без смысла).

##### Состав работ

- Расширить существующий compose: сохранить сервис `db` (тот же volume/пользователь, если не мешает миграциям), добавить `backend`, `bot`, `frontend` с `build` на `devops/*/Dockerfile` и `context` на корень/подпапки согласно ADR.
- Проброс портов: backend (8000), frontend (3000), db при необходимости с хоста.
- Env: использовать `.env` / `.env.example` из корня, документировать обязательные переменные для «полного стека».
- Опционально: профиль `db-only` или `docker compose -f` не требуется, если [Makefile](Makefile) для БД остаётся на том же файле (уточнить в задаче 04).

##### Артефакты

- [docker-compose.yml](../../docker-compose.yml) (замена/расширение текущего)

##### Definition of Done

**Agent self-check**

- [ ] `docker compose config` валиден.
- [ ] `docker compose up` поднимает все сервисы; db healthy до старта зависимых (где задано).

**User check**

- [ ] После `docker compose up` backend отвечает на `/health`, frontend открывается в браузере, бот не падает в логах при валидных токенах (или явно задокументирован smoke без реального Telegram).

---

#### Задача 04: Расширение `Makefile` (стек, логи, health, help) (ит. 1) ✅

##### Цель

Удобные цели: подъём и остановка **полного** стека, статус, логи (всех и по сервису), быстрые проверки (например health), **краткая справка** по целям (`make help` или комментарии `.PHONY` + вывод).

##### Состав работ

- Добавить цели (имена согласовать, примеры): `stack-up`, `stack-down`, `stack-ps` / `stack-status`, `stack-logs`, `stack-logs-SERVICE` или `SERVICE=...`, `stack-health` (запрос к backend `/health`, кроссплатформенно).
- Сохранить обратную совместимость с `backend-db-up` и существующими целями или явно задокументировать миграцию в задаче 07.
- `help` / список целей: перечислить новые stack-* и короткое описание.

##### Артефакты

- [Makefile](../../Makefile)

##### Definition of Done

**Agent self-check**

- [ ] `make -n` / запуск `make help` не ломается; новые цели в `.PHONY`.
- [ ] `make stack-health` завершается 0 при поднятом healthy backend (в CI-окружении опционально пропустить).

**User check**

- [ ] Без чтения исходников ясно, как остановить стек и посмотреть логи одного сервиса.

---

#### Задача 05: Ревью docker-конфигурации (skill **docker-expert**) (ит. 1) ✅

##### Цель

Снизить риск антипаттернов: лишние слои, root в production, слабая изоляция секретов, неоптимальный `.dockerignore`, healthcheck'и.

##### Состав работ

- Прочитать skill **docker-expert** и пройтись чек-листом по `Dockerfile*`, `docker-compose.yml`, `Makefile` stack-целям.
- Зафиксировать findings: критичные — исправить в рамках ит.1; остальное — в backlog/ADR/комментарий в tasklist.
- Краткая заметка (1 страница max) **где** угодно: `docs/tech/docker-review-notes.md` или раздел в summary — по выбору исполнителя.

##### Артефакты

- `docs/tech/docker-review-notes.md` (рекомендуется) или ссылка на PR-комментарии

##### Definition of Done

**Agent self-check**

- [ ] Skill **docker-expert** открыт и применён; список проверенных пунктов есть в заметке.

**User check**

- [ ] Критичные замечания либо исправлены, либо осознанно отложены с номером задачи/ADR.

---

#### Задача 06: Инструкция — локальный запуск через Docker Compose (ит. 1) ✅

##### Цель

Отдельный документ: как с нуля поднять **весь** проект в Docker (env, первый `compose up`, миграции, типичные ошибки, отличия от `make backend-run` + `make frontend-dev`).

##### Состав работ

- Предусловия: Docker / Compose версии, копия `.env` из `.env.example`, переменные для бота/LLM/Telegram.
- Порядок: build → up → `backend-db-migrate` (с хоста с установленным uv или one-off `compose run` — явно описать).
- Команды из `Makefile` и прямые `docker compose` на выбор; troubleshooting (порт занят, db not ready).
- Ссылка на [onboarding.md](../onboarding.md) для контекста «без Docker».

##### Артефакты

- [docs/how-to-docker.md](../how-to-docker.md)

##### Definition of Done

**Agent self-check**

- [ ] Все пути к файлам в документе относительны и проверены.
- [ ] Упомянут `make stack-*` (или итоговые имена из задачи 04).

**User check**

- [ ] Новый участник проходит инструкцию и поднимает стек с первого/второго раза.

---

#### Задача 07: Обновление проектной документации (ит. 1) ✅

##### Цель

Репозиторий согласован: README, архитектура, план, аудит доки — указывают на `devops/`, docker-compose, how-to, tasklist, ограничения (подготовительная фаза, не полный CI/CD).

##### Состав работ

- [README.md](../../README.md): раздел «Docker / полный стек» + ссылка на `how-to-docker.md`.
- [docs/architecture.md](../architecture.md): deployment/ops абзац или обновить таблицу «PostgreSQL» (не только внешний docker-compose).
- [docs/plan.md](../plan.md): строка в таблице «Области» / «Следующие шаги» — ссылка на [tasklist-devops.md](tasklist-devops.md).
- [docs/doc-audit.md](../doc-audit.md): закрытие/обновление строк про Docker-only compose и `.github/workflows` (итерация 2).

##### Артефакты

- Перечисленные markdown-файлы

##### Definition of Done

**Agent self-check**

- [ ] Нет битых внутренних ссылок на новый tasklist и how-to.

**User check**

- [ ] Сводка в README отражает актуальные команды; doc-audit не противоречит факту.

---

### Итерация 2: GitHub Actions — образы в GHCR

> Полноценный CI (lint/test на PR) — **вне** этого tasklist'а, если не сказано иное; фокус — **build + push** образов.

#### Задача 08: Workflow — сборка и публикация образов в GHCR (ит. 2) 📋

##### Цель

Пайплайн GitHub Actions: на push/tag (или `workflow_dispatch`) — **сборка** трёх образов и **push** в **ghcr.io** (GitHub Container Registry), с тегами (например `latest` + `sha`).

##### Состав работ

- Использовать skill **github-actions-templates** при проектировании workflow.
- `GITHUB_TOKEN` / permissions: `contents:read`, `packages:write`; логин в GHCR.
- Матрица или три job'а: backend, bot, frontend; кэш buildkit при возможности.
- Описать в [docs/how-to-docker.md](../how-to-docker.md) или `devops/README.md` ссылку на пакеты и теги.

##### Артефакты

- `.github/workflows/docker-publish.yml` (имя на усмотрение, одно соглашение на репо)

##### Definition of Done

**Agent self-check**

- [ ] Workflow синтаксически валиден; в форке/ветке — dry-run по возможности.
- [ ] В репо задокументировано, **какой** event триггерит публикацию.

**User check**

- [ ] После мержа в main пакеты видны в GitHub Packages; образы pullable.

---

#### Задача 09: Ревью compose для запуска с образами из registry (ит. 2) 📋

##### Цель

Compose-профиль или **override-файл** (`docker-compose.prod-images.yml` / `docker-compose.ghcr.yml` или `profiles: images`) для запуска с **`image: ghcr.io/...`** вместо `build:`, согласованный с тегами из задачи 08.

##### Состав работ

- Не дублировать весь стек: использовать `extends` или YAML anchor по возможности, иначе — явный override + документация.
- Проверить согласованность env и портов с локальным `docker-compose.yml`.
- Skill **docker-expert** — точечно на сети/тома/персистентность db.

##### Артефакты

- Доп. compose (override) + обновление [how-to-docker.md](../how-to-docker.md) (раздел «образы из GHCR»)

##### Definition of Done

**Agent self-check**

- [ ] `docker compose -f ... config` валиден; pull образов без ручного `docker login` **или** шаг login описан.

**User check**

- [ ] Запуск только из registry (без `build` на машине) работает согласно инструкции.

---

#### Задача 10: Локальная проверка полного стека на образах из GHCR (ит. 2) 📋

##### Цель

Подтвердить: `docker pull` (или compose с `image`) + `up` — весь продуктовый набор поднимается **без** локальной сборки Dockerfile.

##### Состав работ

- Очистить/не использовать локальные build-кэши для проверки; указать `docker compose pull` / тег.
- Смоук: `/health`, главная UI, бот (или задокументированный skip без токенов).
- Результат: короткий пункт в [onboarding.md](../onboarding.md) или в [how-to-docker.md](../how-to-docker.md) — «проверено в дату …».

##### Артефакты

- Обновление `docs/how-to-docker.md` и/или `docs/onboarding.md`

##### Definition of Done

**Agent self-check**

- [ ] Сценарий воспроизводим с чистой машиной (кромо секретов в `.env`).

**User check**

- [ ] Выполнен ручной прогон по инструкции; отмечен статус/дата.

---

## Примечания

- **Секреты:** не коммитить; в GHA — GitHub Secrets при необходимости для **сборки**; runtime-секреты — только env на хосте/в compose.
- **Миграции БД** в контейнерах: либо entrypoint, либо отдельный one-off `docker compose run --rm ... alembic upgrade head` — выбрать в задачах 02–03 и описать в задаче 06.
- **Имена образов/репозитория GHCR** — привязать к `github.com` org/user репозитория при реализации задачи 08.
