# Аудит документации — реестр и план

**Назначение:** зафиксировать состояние документации, приоритезировать доработки и отметить закрытые пробелы.

**Обновлено:** 2026-04-25 — P0–P2 (онбординг, архитектура, contributing, AGENTS, README). **CI в репозиторий не добавлялся** (отложено).

---

## 1. Реестр документации

| Файл | Описание | Статус | Проблемы / примечания |
|------|----------|--------|------------------------|
| [README.md](../README.md) | Название, архитектура + ссылка на [architecture.md](architecture.md), prereq, env, старт, тесты, `make`, ссылки на `docs/` | ✅ Актуально | — |
| [docs/architecture.md](architecture.md) | Технарх: схемы mermaid, компоненты, потоки, ссылки | ✅ Добавлено (2026-04-25) | — |
| [docs/onboarding.md](onboarding.md) | Пошаговый гайд новичка (6 разделов) | ✅ Добавлено (2026-04-25) | — |
| [docs/contributing.md](contributing.md) | Ветки, `make check`, коммиты | ✅ Добавлено (2026-04-25) | — |
| [backend/README.md](../backend/README.md) | Backend: старт, тесты, структура, env, ссылки | ✅ Актуально | — |
| [frontend/README.md](../frontend/README.md) | Frontend: env, make/pnpm, структура, стек, ссылки | ✅ Актуально | — |
| `bot/README.md` | — | ❌ Нет (папка `bot/` пустая) | Код бота: `src/ttlg_bot/` — см. [README.md](../README.md), [architecture.md](architecture.md) |
| [docs/vision.md](vision.md) | Архитектурное видение | ✅ Актуально | — |
| [docs/plan.md](plan.md) | Дорожная карта | ✅ Актуально (2026-04-22) | Итерация 6 — 🚧 частично (ожидаемо) |
| [docs/data-model.md](data-model.md) | Модель данных | ✅ Актуально | — |
| [docs/tech/api-contracts.md](tech/api-contracts.md) | HTTP API | ✅ Актуально | — |
| [.env.example](../.env.example) | Переменные окружения (корень) | ✅ Актуально | — |
| [frontend/.env.local.example](../frontend/.env.local.example) | Env для Next.js | ✅ Актуально | — |
| [Makefile](../Makefile) | Команды dev/test/lint/БД/frontend | ✅ Актуально | `check` = без `frontend-test` (см. §6) |
| [docker-compose.yml](../docker-compose.yml) | Только PostgreSQL | ✅ Актуально | dev-only; prod — см. P3 / vision |
| [.cursor/rules/conventions.mdc](../.cursor/rules/conventions.mdc) | Конвенции для агентов | ✅ Актуально | — |
| [.cursor/rules/workflow.mdc](../.cursor/rules/workflow.mdc) | Процесс (Plan, согласования) | ✅ Актуально | **Расхождение с фактом:** в правиле сказано «нет вложенных `tasks/`»; в репо есть `docs/tasks/` — см. §6 |
| [frontend/AGENTS.md](../frontend/AGENTS.md) | Подсказка AI: Next + проект, `src/`, `make`, MSW, middleware | ✅ Расширено (2026-04-25) | — |
| [frontend/CLAUDE.md](../frontend/CLAUDE.md) | Ссылка на AGENTS | ✅ Ок | — |
| [docs/idea.md](idea.md) | Идея продукта | ✅ Актуально | — |
| [docs/integrations.md](integrations.md) | Интеграции, smoke | ✅ Актуально | — |
| [docs/tech/db-guide.md](tech/db-guide.md) | Справка по БД | ✅ Актуально | — |
| [docs/api-conventions.md](api-conventions.md) | HTTP-конвенции | ✅ Актуально | — |
| [docs/spec/frontend-requirements.md](spec/frontend-requirements.md) | UI-спека | ✅ Актуально | — |
| [docs/adr/](adr/) | ADR 001–004 | ✅ Актуально | — |
| [docs/openapi.json](openapi.json) | OpenAPI (экспорт) | ✅ Доп. артефакт | `make openapi-export` |
| [docs/tasks/](tasks/) | Tasklists, impl | ✅ Рабочие материалы | Онбординг: [onboarding.md](onboarding.md) п.4–5 |
| `.github/workflows/` | CI | ❌ Нет | Запланировано отдельно — см. P1 |

---

## 2. Аудит «запускаемости»

| Шаг | Статус | Примечание |
|-----|--------|------------|
| Установка системных зависимостей | ✅ Есть | [README.md § Системные требования](../README.md) + [onboarding.md](onboarding.md) |
| Настройка окружения | ✅ Есть | Таблица **Переменные окружения** в [README.md](../README.md) |
| Настройка фронтенд-env | ✅ Есть | `frontend/.env.local` |
| Запуск БД | ✅ Есть | `make backend-db-up` |
| Запуск backend | ✅ Есть | `make backend-run` + [backend/README.md](../backend/README.md) |
| Запуск frontend | ✅ Есть | `make frontend-dev` + [frontend/README.md](../frontend/README.md) |
| Запуск бота | ✅ Есть | `make run` (код: `src/ttlg_bot/`) |
| Тесты | ✅ Есть | `make backend-test`, `make bot-test`, `make frontend-test` |
| Проверка работоспособности | ✅ Есть | `GET /health`, `/docs` — [onboarding.md](onboarding.md) §3 |
| Качество кода | ✅ Есть | `make lint`, `make format`, `make frontend-lint`, `make check` |
| CI на push/PR | ❌ | Не автоматизировано — см. бэклог P1 |

---

## 3. Закрыто ранее (2026-04-25, критичные пробелы)

- [backend/README.md](../backend/README.md), замена [frontend/README.md](../frontend/README.md), системные требования и `frontend/.env.local` в [README.md](../README.md).

**Также закрыто (P0, P2 и часть P1, 2026-04-25):**

**P0 (документация):** [docs/architecture.md](architecture.md), [docs/onboarding.md](onboarding.md), согласование [README.md](../README.md) (env, ссылки, без CI).

**P1.2 (contributing):** [docs/contributing.md](contributing.md) (ветки, `make check`, коммиты).

**P2:** [frontend/AGENTS.md](../frontend/AGENTS.md); в [README.md](../README.md) явно указано расположение бота `src/ttlg_bot/`.

> **P1.1 (GitHub Actions** — `make check` на push/PR) **отложено**, в репозиторий не коммитилось; см. §4.

---

## 4. Приоритезированный бэклог

### P1 — CI (высокий эффект, когда будете готовы)

| # | Действие | Зачем |
|---|----------|--------|
| 1.1 | Добавить GitHub Actions: `make check` (или matrix: Ruff+pytest+eslint) на push/PR | Один «зелёный» барьер для всех, без ручного прогона |

### P3 — по желанию

| # | Действие | Зачем |
|---|----------|--------|
| 3.1 | Dockerfile’ы + compose full-stack | Деплой/демо без локальной ручной сборки |
| 3.2 | `engines` в [frontend/package.json](../frontend/package.json) (`node`, `pnpm`) | Жёстче зафиксировать версии (удобно под будущий CI) |

---

## 5. Критерий «готово» для бэклога

- **P1:** в репо есть workflow, `make check` (или эквивалент) зелёный на типичном PR.
- **P2:** по README + AGENTS новый участник поднимает три компонента — см. [onboarding.md](onboarding.md) (выполнено по доке).
- **P3:** зафиксировано решение «нужен ли docker для prod» в vision/plan или в отдельном ADR.

---

## 6. Соответствие коду и уточнения

1. **`make check` не вызывает `frontend-test`:** [Makefile:19](../Makefile) — `check: lint backend-test bot-test frontend-lint`. В README, contributing и onboarding согласовано.

2. **`.cursor/rules/workflow.mdc`:** про «нет вложенного `tasks/`» vs **`docs/tasks/`** — [onboarding.md](onboarding.md) п.4–5 и [plan.md](plan.md).

3. **Пустой `bot/`:** навигация на `src/ttlg_bot/` — в README и [architecture.md](architecture.md).
