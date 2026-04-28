# Frontend — веб-клиент TTLG

Next.js 16 приложение для ученика и преподавателя. Тонкий клиент над backend API.

## Быстрый старт

```bash
# Из корня репозитория
cp frontend/.env.local.example frontend/.env.local   # NEXT_PUBLIC_API_URL, AUTH_SECRET
pnpm install                                          # lockfile: корневой pnpm-lock.yaml (workspace)

make backend-run       # в отдельном терминале — нужен работающий backend
make frontend-dev      # dev-сервер → http://localhost:3000
```

Для полной работы потребуется запущенный backend с заполненной БД — см. [корневой README](../README.md#backend-fastapi).

## Переменные окружения

Скопируйте `.env.local.example` → `.env.local` (файл не коммитить):

| Переменная | Описание |
|------------|----------|
| `NEXT_PUBLIC_API_URL` | URL backend API, по умолчанию `http://localhost:8000` |
| `AUTH_SECRET` | JWT-секрет, должен совпадать с `SECRET_KEY` в backend `.env` |
| `NEXT_PUBLIC_SITE_URL` | Базовый URL фронта, по умолчанию `http://localhost:3000` |

## Команды

```bash
make frontend-dev      # dev-сервер с hot reload
make frontend-build    # production-сборка
make frontend-lint     # ESLint
make frontend-test     # Vitest (unit + integration с MSW)
```

Или напрямую через pnpm:

```bash
pnpm --filter frontend dev
pnpm --filter frontend test
```

## Структура

```
frontend/src/
├── app/               # Next.js App Router
│   ├── (auth)/        # страницы входа/выхода
│   ├── (app)/         # защищённые страницы (dashboard, students, schedule…)
│   └── api/           # Route Handlers (proxy к backend)
├── components/        # UI-компоненты (shadcn/ui + кастомные)
└── lib/               # api-клиент, типы, утилиты, константы
```

## Стек

- **Next.js 16**, **React 19**, **TypeScript**
- **Tailwind CSS 4**, **shadcn/ui** (Base UI + Radix)
- **Vitest** + **Testing Library** + **MSW** для тестов
- **react-hook-form** + **Zod** для форм
- **pnpm** (workspace в корне репо)

## Документация

- [Требования к UI (спецификация экранов)](../docs/spec/frontend-requirements.md)
- [HTTP API контракты](../docs/tech/api-contracts.md)
- [Задачи frontend](../docs/tasks/tasklist-frontend.md)
