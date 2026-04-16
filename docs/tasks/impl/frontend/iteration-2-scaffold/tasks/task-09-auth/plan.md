# Задача 09 — Форма входа и защищённые роуты: план

## Цель

Реализовать страницу `/login` с формой (email + пароль + роль); аутентификацию через Server Action → `POST /v1/auth/login`; хранение JWT в httpOnly cookie; middleware для защиты роутов и редиректов по роли.

## Что меняется

| Файл | Тип | Описание |
|------|-----|----------|
| `frontend/src/app/(auth)/login/page.tsx` | **новый** | Страница входа — Server Component |
| `frontend/src/app/actions/auth.ts` | **новый** | Server Action: login/logout через backend API |
| `frontend/src/app/api/auth/logout/route.ts` | **новый** | Route Handler: очистка cookie + редирект |
| `frontend/src/middleware.ts` | **новый** | Проверка cookie, редирект по роли |
| `frontend/src/lib/auth.ts` | **новый** | `getSession()`, `getUser()` с `React.cache()` |

## Зависимости задачи

- Задача 07 завершена: `frontend/` существует, shadcn компоненты установлены.
- Задача 08 завершена: `ThemeToggle` доступен.
- Backend `POST /v1/auth/login` принимает `{ email, password, role }`, возвращает `200` + устанавливает httpOnly cookie **или** возвращает токен в теле (уточнить по `docs/tech/api-contracts.md`).

> По контракту: `POST /v1/auth/login` response `200`: `{ "user": { "id", "name", "role" } }` без токена в JSON при cookie-only модели. Токен устанавливается через `Set-Cookie` backend'ом. Если backend не устанавливает cookie сам — Server Action должен сделать это явно через `cookies().set(...)` из `next/headers`.

## Архитектурные решения

### Cookie-стратегия

Backend из итерации 1 использует JWT. Нужно уточнить при реализации: устанавливает ли backend `Set-Cookie` сам при логине, или токен приходит в теле и Next.js должен его сохранить. По контракту — модель cookie-only, значит либо:
- **Вариант A:** Backend устанавливает `Set-Cookie` — Next.js просто проксирует ответ.
- **Вариант B:** Backend возвращает токен в теле — Server Action получает токен и сам вызывает `cookies().set('token', jwt, { httpOnly: true, secure: ..., sameSite: 'lax' })`.

В задаче реализовать Вариант B (явная установка cookie через `next/headers`) — это надёжнее и не зависит от конфигурации CORS/Proxy.

### Структура формы (shadcn)

Форма входа — `"use client"` Client Component, встроенная в Server Component страницу. Причина: необходимость `useFormState` / `useFormStatus` для pending-состояния.

```
(auth)/login/
  page.tsx         ← Server Component (только оболочка, import LoginForm)
  _login-form.tsx  ← Client Component ("use client")
```

Компоненты shadcn:
- `Card` — обёртка карточки
- `FieldGroup + Field + Label + Input` — поля формы (если Field доступен в shadcn v4)
- `Button` с `disabled` в pending
- `Alert` — ошибки от сервера
- Toggle ролей: две `Button variant="outline"` / `variant="default"` для выбора `teacher` / `student`

### Server Action

`frontend/src/app/actions/auth.ts`:

```ts
"use server"

import { cookies } from "next/headers"
import { redirect } from "next/navigation"

export async function loginAction(formData: FormData) {
  const email = formData.get("email")?.toString().trim() ?? ""
  const password = formData.get("password")?.toString() ?? ""
  const role = formData.get("role")?.toString() ?? ""

  // Валидация до запроса
  if (!email || !password || !role) {
    return { error: "Заполните все поля" }
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { error: "Некорректный формат e-mail" }
  }

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, role }),
  })

  if (!res.ok) {
    return { error: "Неверный логин или пароль" }
  }

  // Если backend возвращает токен в теле:
  const data = await res.json()
  const token = data.token  // уточнить по реализации backend
  if (token) {
    cookies().set("token", token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24,  // 24h
    })
  }

  redirect(role === "teacher" ? "/teacher/calendar" : "/student/schedule")
}
```

### Route Handler (logout)

`frontend/src/app/api/auth/logout/route.ts`:

```ts
import { NextResponse } from "next/server"
import { cookies } from "next/headers"

export async function POST() {
  cookies().delete("token")
  return NextResponse.redirect(new URL("/login", process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"))
}
```

### Middleware

`frontend/src/middleware.ts` — тонкий, только cookie-проверка:

```ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value
  const { pathname } = request.nextUrl

  if (!token && pathname !== "/login") {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  // Дополнительный роутинг по роли — в задаче 11
  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
}
```

Роль из JWT декодируется в задаче 11 для перекрёстного редиректа.

### lib/auth.ts

```ts
import { cache } from "react"
import { cookies } from "next/headers"

export const getSession = cache(async () => {
  const token = cookies().get("token")?.value
  if (!token) return null
  return { token }
})

export const getUser = cache(async () => {
  const session = await getSession()
  if (!session) return null

  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/v1/auth/me`, {
    headers: { Cookie: `token=${session.token}` },
    cache: "no-store",
  })
  if (!res.ok) return null
  return res.json() as Promise<{ id: string; name: string; role: "teacher" | "student" }>
})
```

## Пошаговый план реализации

1. Создать `src/lib/auth.ts` с `getSession` и `getUser` (`React.cache`)
2. Создать Server Action `src/app/actions/auth.ts`
3. Создать Route Handler `src/app/api/auth/logout/route.ts`
4. Создать страницу `src/app/(auth)/login/page.tsx` + Client Component формы
5. Создать `src/middleware.ts` с базовой проверкой cookie
6. Проверить: dev-сервер, `/login`, вход преподавателем, httpOnly cookie в DevTools

## Запреты

- JWT **не хранить** в `localStorage` или `sessionStorage`.
- `getUser()` не вызывать без `React.cache()` — каждый вызов создаёт HTTP-запрос.
- В форме не дублировать логику валидации в Server Action и на клиенте независимо — клиентская для UX, серверная обязательна.
- Middleware не должен содержать тяжёлой логики (DB-запросы, полный JWT-verify с импортом `jose`/`jsonwebtoken` — Edge Runtime ограничен).

## Риски

| Риск | Митигация |
|------|-----------|
| Backend устанавливает `Set-Cookie` сам — дублирование | Проверить заголовки ответа при логине; при наличии `Set-Cookie` от backend — убрать явный `cookies().set` из Action |
| JWT decode в Edge Runtime (middleware) | Использовать `jose` (Edge-совместимый) или хранить роль отдельно в cookie при логине |
| CORS при fetch из Server Action | Server Actions выполняются на сервере — CORS не применяется |

## Definition of Done

- [ ] `/login` — страница с формой (email + пароль + роль + кнопка «Войти»)
- [ ] Успешный вход teacher → редирект на `/teacher/calendar`
- [ ] JWT в httpOnly cookie (видно в DevTools → Application → Cookies, `HttpOnly: true`)
- [ ] Прямой переход на `/teacher/calendar` без cookie → редирект на `/login`
- [ ] `getUser()` обёрнут в `React.cache()`
- [ ] Кнопка logout очищает cookie и редиректит на `/login`
- [ ] TypeScript-ошибок нет
