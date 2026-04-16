# Задача 11 — Маршрутизация по ролям и Makefile-цели: план

## Цель

Создать страницы-заглушки всех экранов с `loading.tsx`; настроить middleware для ролевой маршрутизации и блокировки перекрёстного доступа; добавить `frontend-*` цели в корневой `Makefile`.

## Что меняется

| Файл | Тип | Описание |
|------|-----|----------|
| `frontend/src/app/(app)/teacher/calendar/page.tsx` | **новый** | Заглушка (Server Component) |
| `frontend/src/app/(app)/teacher/calendar/loading.tsx` | **новый** | Skeleton-экран |
| `frontend/src/app/(app)/teacher/students/page.tsx` | **новый** | Заглушка |
| `frontend/src/app/(app)/teacher/students/loading.tsx` | **новый** | Skeleton-экран |
| `frontend/src/app/(app)/teacher/settings/page.tsx` | **новый** | Заглушка |
| `frontend/src/app/(app)/teacher/settings/loading.tsx` | **новый** | Skeleton-экран |
| `frontend/src/app/(app)/student/schedule/page.tsx` | **новый** | Заглушка |
| `frontend/src/app/(app)/student/schedule/loading.tsx` | **новый** | Skeleton-экран |
| `frontend/src/middleware.ts` | **изменение** | Добавить ролевой редирект (расширение задачи 09) |
| `Makefile` | **изменение** | Добавить `frontend-dev`, `frontend-build`, `frontend-lint`, `frontend-test`; обновить `check` |

## Зависимости задачи

- Задача 09: `middleware.ts` создан с базовой cookie-проверкой; `lib/auth.ts` с `getSession()`.
- Задача 10: layout для `(app)/` готов.

## Страницы-заглушки

Все страницы — **Server Components** по умолчанию. `"use client"` не добавлять.

Пример заглушки (`teacher/calendar/page.tsx`):

```tsx
export default function CalendarPage() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold">Календарь</h1>
      <p className="text-muted-foreground mt-2">Экран будет реализован в итерации 3.</p>
    </div>
  )
}
```

Аналогично для остальных трёх страниц (заголовки: «Ученики», «Настройки», «Моё расписание»).

## loading.tsx — Skeleton-экраны

Файловая конвенция App Router: `loading.tsx` автоматически оборачивает `page.tsx` в `<Suspense>`.

Содержимое — **Skeleton из shadcn**, не `<div className="animate-pulse">`:

```tsx
import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="p-6 flex flex-col gap-4">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-64 w-full" />
    </div>
  )
}
```

Каждый `loading.tsx` — в отдельном файле в своей директории роута.

## Расширение middleware — ролевой редирект

Добавить в `frontend/src/middleware.ts` декодирование роли из JWT и перекрёстный редирект.

Для декодирования в Edge Runtime использовать `jose`:

```bash
pnpm --filter frontend add jose
```

Расширенный middleware:

```ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { jwtVerify } from "jose"

const JWT_SECRET = new TextEncoder().encode(process.env.JWT_SECRET ?? "")

export async function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value
  const { pathname } = request.nextUrl

  // Публичные пути
  if (pathname === "/login" || pathname.startsWith("/_next") || pathname.startsWith("/api/auth")) {
    return NextResponse.next()
  }

  if (!token) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  // Декодируем роль
  let role: string
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET)
    role = (payload as { role?: string }).role ?? ""
  } catch {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  // Перекрёстный доступ
  if (pathname.startsWith("/teacher") && role !== "teacher") {
    return NextResponse.redirect(new URL("/student/schedule", request.url))
  }
  if (pathname.startsWith("/student") && role !== "student") {
    return NextResponse.redirect(new URL("/teacher/calendar", request.url))
  }

  // Редирект с корня
  if (pathname === "/") {
    return NextResponse.redirect(
      new URL(role === "teacher" ? "/teacher/calendar" : "/student/schedule", request.url)
    )
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
}
```

> `JWT_SECRET` должен совпадать с `SECRET_KEY` в backend. Добавить в `frontend/.env.local.example`:
> ```
> JWT_SECRET=your-secret-key-here
> ```

## Makefile — новые цели

Добавить в корневой `Makefile`:

```makefile
.PHONY: ... frontend-dev frontend-build frontend-lint frontend-test

frontend-dev:
	pnpm --filter frontend dev

frontend-build:
	pnpm --filter frontend build

frontend-lint:
	pnpm --filter frontend lint

frontend-test:
	pnpm --filter frontend test
```

Обновить `.PHONY` и цель `check`:

```makefile
check: lint backend-test bot-test frontend-lint
```

## Пошаговый план реализации

1. Создать 4 страницы-заглушки (Server Components)
2. Создать 4 `loading.tsx` с Skeleton
3. Установить `jose`: `pnpm --filter frontend add jose`
4. Расширить `middleware.ts`: роль из JWT, перекрёстный редирект, редирект с `/`
5. Добавить `JWT_SECRET` в `.env.local.example`
6. Обновить `Makefile`: 4 новые цели + `check`
7. Проверить: `make frontend-lint` (без ошибок), ролевой редирект

## Запреты

- Не добавлять `"use client"` в page.tsx заглушки — это Server Components.
- Не использовать `animate-pulse div` в loading.tsx — только `<Skeleton>`.
- Не дублировать cookie-проверку в page.tsx — она только в middleware и `lib/auth.ts`.
- Не определять компоненты внутри `page.tsx` — каждый компонент в своём файле (правило `rerender-no-inline-components`).

## Риски

| Риск | Митигация |
|------|-----------|
| `jose` не верифицирует токен (алгоритм/секрет не совпадают) | Взять `JWT_SECRET` из backend `.env`; в dev можно задать общий секрет через `.env.local` |
| pnpm workspace: `pnpm --filter frontend` не находит пакет | Убедиться, что `pnpm-workspace.yaml` содержит `"frontend"` и `frontend/package.json` существует |
| `make check` падает из-за frontend-lint (нет `frontend/`) | Задача 11 выполняется последней в итерации; к этому моменту `frontend/` существует |

## Definition of Done

- [ ] 4 страницы-заглушки (teacher: calendar, students, settings; student: schedule) созданы как Server Components
- [ ] 4 `loading.tsx` с `<Skeleton>` — нет `animate-pulse div`
- [ ] Middleware: teacher → `/student/*` редиректит на `/teacher/calendar`; student → `/teacher/*` редиректит на `/student/schedule`
- [ ] Логика cookie не дублируется — переиспользует `lib/auth.ts`
- [ ] `JWT_SECRET` добавлен в `.env.local.example`
- [ ] `make frontend-dev`, `make frontend-build`, `make frontend-lint`, `make frontend-test` добавлены в `Makefile`
- [ ] `make check` включает `frontend-lint`
- [ ] `make frontend-lint` проходит без ошибок
