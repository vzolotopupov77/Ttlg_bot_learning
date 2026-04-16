# Итерация 2 — Каркас frontend-проекта: план

## Цель

Создать и настроить `frontend/` с нуля: инициализировать Next.js App Router + TypeScript + shadcn/ui + Tailwind CSS, настроить темы (light/dark без FOUC), реализовать форму входа с JWT-аутентификацией, общий layout с навигацией по ролям, маршрутизацию и Makefile-цели.

## Ценность

После итерации разработчик может запустить `make frontend-dev`, войти под преподавателем или учеником, увидеть навигацию с правильными пунктами и заглушки всех экранов. Backend API полностью готов (итерации 0–1 завершены).

---

## Предусловия

| Предусловие | Статус |
|-------------|--------|
| Backend API (auth, students, teacher, settings) реализован | ✅ Итерация 1 |
| `POST /v1/auth/login` возвращает JWT (httpOnly cookie) | ✅ |
| `GET /v1/auth/me` возвращает `id`, `name`, `role` | ✅ |
| API-контракты зафиксированы в `docs/tech/api-contracts.md` | ✅ |
| `frontend/` директория отсутствует, `pnpm-workspace.yaml` — нет | создаётся в задаче 07 |

---

## Состав задач

| № | Задача | Зависит от |
|---|--------|-----------|
| 07 | Инициализация Next.js + shadcn/ui | — |
| 08 | Темы: light/dark, CSS-переменные | 07 |
| 09 | Форма входа + защищённые роуты | 07, 08 |
| 10 | Layout: sidebar, header, mobile drawer | 07, 08, 09 |
| 11 | Маршрутизация по ролям + Makefile | 07, 09, 10 |

Задачи выполняются последовательно: каждая опирается на результат предыдущей.

---

## Затрагиваемые файлы и инфраструктура

### Новые файлы/директории

```
frontend/                          # новый Next.js проект
  package.json
  pnpm-lock.yaml
  next.config.ts
  tsconfig.json
  components.json                  # shadcn конфиг
  .env.local.example
  src/
    app/
      layout.tsx                   # корневой, Server Component
      not-found.tsx
      globals.css                  # CSS-переменные (только семантические токены)
      (auth)/
        login/
          page.tsx                 # форма входа
      (app)/
        layout.tsx                 # layout аутентифицированной зоны
        error.tsx                  # "use client" Error Boundary
        teacher/
          calendar/page.tsx + loading.tsx
          students/page.tsx + loading.tsx
          settings/page.tsx + loading.tsx
        student/
          schedule/page.tsx + loading.tsx
      actions/
        auth.ts                    # Server Action ("use server")
      api/
        auth/logout/route.ts       # Route Handler
    components/
      providers.tsx                # ThemeProvider ("use client")
      theme-toggle.tsx
      sidebar.tsx
      header.tsx
      mobile-nav.tsx
    lib/
      auth.ts                      # getSession(), getUser() с React.cache()
    middleware.ts
pnpm-workspace.yaml                # новый (workspace: [frontend])
Makefile                           # добавлены frontend-* цели
```

### Изменяемые файлы

| Файл | Изменение |
|------|-----------|
| `Makefile` | Добавить `frontend-dev`, `frontend-build`, `frontend-lint`, `frontend-test`; обновить цель `check` |
| `pnpm-workspace.yaml` | Создать новый (монорепо с `frontend/`) |

---

## Ключевые технические решения

### Аутентификация
- **JWT в httpOnly cookie** — устанавливается Server Action `auth.ts` через `cookies()` из `next/headers`.
- Декодирование роли в middleware — только для редиректа; тяжёлой логики в middleware нет.
- `getUser()` обёрнут в `React.cache()` — без дублирующих DB/API-запросов за один render.
- Кнопка «Выйти» → Route Handler `POST /api/auth/logout` → очищает cookie → редирект на `/login`.

### Темы
- `next-themes` с `attribute="class"`, `defaultTheme="system"`.
- CSS-переменные только в `globals.css` — **только семантические токены** shadcn (`--background`, `--foreground`, `--primary` и т.д.), без raw-цветов.
- `suppressHydrationWarning` на `<html>` — FOUC исключён.

### Server/Client split
- Все `page.tsx` и `layout.tsx` — Server Components по умолчанию.
- `"use client"` только у: `providers.tsx`, `theme-toggle.tsx`, `header.tsx` (интерактивность), `mobile-nav.tsx`, `error.tsx`, форма входа (состояние pending/ошибки).
- `sidebar.tsx` — Server Component (статические ссылки); активный пункт через `usePathname()` требует Client Component только для highlights — изолировать в отдельный `NavLink` Client Component.

### Маршрутизация
- Route groups: `(auth)` — без layout (только `/login`); `(app)` — с общим layout.
- Middleware: проверка cookie → при отсутствии `redirect('/login')`; при наличии — роль из JWT → редирект на стартовую страницу своей роли.

### pnpm workspace
- `pnpm-workspace.yaml` в корне: `packages: ["frontend"]`.
- Все frontend-команды в Makefile через `pnpm --filter frontend <cmd>`.

---

## Риски

| Риск | Митигация |
|------|-----------|
| shadcn CLI может не поддерживать Tailwind v4 в стабильной версии | Проверить `components.json` после `init`; при необходимости использовать Tailwind v3-пресет |
| JWT cookie не передаётся на backend при dev (разные порты) | `NEXT_PUBLIC_API_URL` указывает на `http://localhost:8000`; fetch из Server Actions не ограничен CORS; при необходимости настроить proxy в `next.config.ts` |
| `next-themes` hydration mismatch в Strict Mode | Решается `suppressHydrationWarning` + `attribute="class"` — стандартный паттерн |

---

## Definition of Done итерации

- [x] `make frontend-dev` запускается, `http://localhost:3000` открывается
- [x] `/login` — видна форма входа; вход под преподавателем → `/teacher/calendar`
- [x] Тема переключается без мигания при перезагрузке
- [x] Sidebar показывает правильные пункты по роли
- [x] Mobile drawer (Sheet) работает, `SheetTitle` присутствует
- [x] Прямой переход teacher на `/student/*` → редирект
- [x] `make frontend-lint` проходит без ошибок
- [x] `make check` включает `frontend-lint`
- [x] TypeScript-ошибок нет; barrel-файлов нет

Проверка зафиксирована в [summary итерации](summary.md) (автоматические команды + ручной смоук).
