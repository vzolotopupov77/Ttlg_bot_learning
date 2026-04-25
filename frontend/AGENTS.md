<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Контекст проекта (TTLG)

Репозиторий — **monorepo** (корневой `pnpm` + Python workspace `uv`).

## Где фронтенд

- **Исходники приложения:** `frontend/src/` (App Router, `app/`, `components/`, `lib/`, тесты рядом или в `__tests__/`).
- **Сборка и скрипты:** `frontend/package.json`, корневой `pnpm-workspace.yaml` — **зависимости ставить из корня:** `pnpm install`, запуск: `make frontend-dev` (эквивалент `pnpm --filter frontend dev`).

## Backend и договоры

- API описан в [docs/tech/api-contracts.md](../docs/tech/api-contracts.md) и [docs/openapi.json](../docs/openapi.json).
- Базовый URL фронта к API: `NEXT_PUBLIC_*` в `frontend/.env.local` (пример: `frontend/.env.local.example`).

## make-команды (выполняйте в Git Bash / WSL на Windows)

| Команда | Назначение |
|---------|------------|
| `make frontend-dev` | dev-сервер |
| `make frontend-build` | production build |
| `make frontend-lint` | ESLint (входит в `make check`) |
| `make frontend-test` | Vitest — **входит в `make check`? Нет; запускать отдельно при смене фронта** |
| `make check` | линт Python + тесты бота/бекенда + `frontend-lint` |

## Паттерны, принятые в репо

- **BFF-прокладка под запрос** не вводим без согласования: клиент ориентирован на **прямой** вызов FastAPI, если иное не оговорено в [api-contracts.md](../docs/tech/api-contracts.md).
- **`middleware.ts`** — редиректы/сессия; не дублировать бизнес-логику backend (роли, права) только в middleware без проверки в API.
- **MSW** — для Vitest-интеграций, изоляция от живого API; см. `frontend/src/test/setup.ts` и существующие `*.test.tsx`. Не подменяйте реальные вызовы в production-коде.
- **Компоненты UI:** shadcn/Tailwind по текущему стеку; не добавляйте тяжёлые UI-библиотеки без причины.

## Документация для людей

- [../docs/onboarding.md](../docs/onboarding.md), [../docs/architecture.md](../docs/architecture.md), [../README.md](../README.md), [../frontend/README.md](README.md).
