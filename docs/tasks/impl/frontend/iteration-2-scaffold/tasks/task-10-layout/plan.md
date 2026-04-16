# Задача 10 — Общий layout: навигация, header, drawer: план

## Цель

Реализовать общий layout для аутентифицированных пользователей: боковая навигация (desktop) с фильтрацией по роли, мобильный Sheet-drawer, header с ThemeToggle и кнопкой выхода.

## Что меняется

| Файл | Тип | Описание |
|------|-----|----------|
| `frontend/src/app/(app)/layout.tsx` | **новый** | Server Component; оборачивает все аутентифицированные страницы |
| `frontend/src/app/(app)/error.tsx` | **новый** | `"use client"` Error Boundary |
| `frontend/src/components/sidebar.tsx` | **новый** | Desktop навигация по ролям |
| `frontend/src/components/nav-link.tsx` | **новый** | Client Component: активный пункт через `usePathname()` |
| `frontend/src/components/header.tsx` | **новый** | `"use client"`: ThemeToggle, Avatar, кнопка выхода |
| `frontend/src/components/mobile-nav.tsx` | **новый** | `"use client"`: Sheet с навигацией |

## Зависимости задачи

- Задача 07: shadcn компоненты установлены (Sheet, Avatar, Separator, Button, Skeleton).
- Задача 08: `ThemeToggle` доступен.
- Задача 09: `getUser()` из `lib/auth.ts` доступен.

## Навигационные пункты по ролям

| Роль | Пункты |
|------|--------|
| `teacher` | Календарь (`/teacher/calendar`), Ученики (`/teacher/students`), Настройки (`/teacher/settings`) |
| `student` | Моё расписание (`/student/schedule`) |

## Архитектурные решения

### Server/Client split

- `layout.tsx` — **Server Component**: вызывает `getUser()`, передаёт `{ name, role }` в Client Components.
- `sidebar.tsx` — **Server Component**: статическая структура, рендерит `NavLink` для каждого пункта.
- `nav-link.tsx` — **Client Component** (`"use client"`): `usePathname()` для активного состояния.
- `header.tsx` — **Client Component**: `ThemeToggle` + кнопка выхода (требует onClick).
- `mobile-nav.tsx` — **Client Component**: управляет состоянием открытия Sheet.

Принцип `server-serialization`: `layout.tsx` передаёт в клиентские компоненты только `name: string` и `role: "teacher" | "student"` — не весь объект пользователя.

### Ленивая загрузка MobileNav

```tsx
// в layout.tsx или header.tsx
import dynamic from "next/dynamic"
const MobileNav = dynamic(() => import("@/components/mobile-nav"), { ssr: false })
```

`MobileNav` загружается только при viewport < 768px (via CSS `flex md:hidden`); `ssr: false` убирает его из серверного bundle.

### Sidebar структура

```
sidebar.tsx (Server Component)
  LogoBlock (статический, вынести из компонента)
  nav items → NavLink (Client Component)
  Separator
  LogoutButton (Client Component)
```

Статические данные (иконки, лейблы навигации) — определить **вне** компонента как константы (правило `rendering-hoist-jsx`).

### Sheet (MobileNav) — доступность

`SheetContent` должен содержать `SheetTitle` (даже скрытый):

```tsx
<Sheet>
  <SheetTrigger asChild>
    <Button variant="ghost" size="icon" aria-label="Открыть меню">
      <Menu className="size-4" />
    </Button>
  </SheetTrigger>
  <SheetContent side="left">
    <SheetTitle className="sr-only">Навигация</SheetTitle>
    {/* те же NavLink что в sidebar */}
  </SheetContent>
</Sheet>
```

### Avatar

```tsx
<Avatar>
  <AvatarFallback>{name.slice(0, 2).toUpperCase()}</AvatarFallback>
</Avatar>
```

`AvatarFallback` обязателен всегда (у нас нет URL аватара).

### Кнопка выхода

Вызывает `fetch('/api/auth/logout', { method: 'POST' })` → Route Handler из задачи 09 очищает cookie и редиректит.

### Адаптивность

- Sidebar: `hidden md:flex flex-col w-64`
- Header: hamburger `flex md:hidden`
- Разделители между группами nav: `<Separator />` (не `<hr>` и не `<div className="border-t">`)
- Вместо `space-x-*` / `space-y-*` — `gap-*` (правило shadcn)

## Пошаговый план реализации

1. Создать `(app)/layout.tsx` — Server Component с `getUser()`, статический `<Sidebar>` и `<Header>`
2. Создать `(app)/error.tsx` — `"use client"` с `reset` prop
3. Создать `nav-link.tsx` — Client Component с `usePathname()` и `cn()`
4. Создать `sidebar.tsx` — Server Component с иконками и `NavLink`
5. Создать `header.tsx` — Client Component с `ThemeToggle`, Avatar, logout
6. Создать `mobile-nav.tsx` — Client Component с Sheet + SheetTitle
7. Подключить `MobileNav` через `next/dynamic` в header или layout
8. Проверить: dev-сервер, `/teacher/calendar`, мобильный viewport

## Компоненты shadcn для добавления (если ещё не установлены)

```bash
pnpm --filter frontend dlx shadcn@latest add avatar
pnpm --filter frontend dlx shadcn@latest add sidebar  # если есть в registry
```

> Перед добавлением проверить: `pnpm --filter frontend dlx shadcn@latest search @shadcn -q "sidebar"` — если есть готовый компонент, использовать его вместо кастомного.

## Запреты

- Не использовать `<hr>` или `<div className="border-t">` для разделителей — только `<Separator>`.
- Не использовать `space-x-*` / `space-y-*` — только `gap-*`.
- Не определять `NavLink` внутри `Sidebar` (нарушение `rerender-no-inline-components`).
- `MobileNav` — отдельный файл, не в `header.tsx`.

## Риски

| Риск | Митигация |
|------|-----------|
| shadcn `sidebar` компонент может не существовать | Реализовать кастомный, используя shadcn-примитивы |
| `usePathname()` в sidebar требует Client — весь sidebar становится клиентским | Изолировать только `NavLink` как Client Component, sidebar остаётся Server Component |
| Avatar без src в shadcn может показывать пустой div | Всегда передавать `AvatarFallback` |

## Definition of Done

- [ ] `layout.tsx` — Server Component; Client Components получают только `name` и `role`
- [ ] `error.tsx` — `"use client"`, принимает `{ error, reset }`
- [ ] Sidebar: 3 пункта для teacher, 1 для student; активный пункт подсвечен через `usePathname()`
- [ ] Mobile (≤768px): sidebar скрыт, hamburger открывает Sheet с `SheetTitle`
- [ ] `Avatar` содержит `AvatarFallback`; иконки из `iconLibrary`
- [ ] `MobileNav` загружается через `next/dynamic`
- [ ] Нет `space-x-*`/`space-y-*`; нет raw `<hr>`
- [ ] `ThemeToggle` и logout работают
- [ ] TypeScript-ошибок нет
