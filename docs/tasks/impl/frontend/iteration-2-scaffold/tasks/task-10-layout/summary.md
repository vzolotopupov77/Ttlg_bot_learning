# Задача 10 — Общий layout: summary

## Статус

✅ Done

## Результат

- `src/app/(app)/layout.tsx`: Server Component, `getUser()`, `Sidebar` + `Header` + `main`.
- `src/app/(app)/error.tsx`: клиентский Error Boundary с `reset`.
- Компоненты: `sidebar.tsx`, `header.tsx`, `mobile-nav.tsx`, `nav-link.tsx`, `logout-button.tsx`.
- `MobileNav` подключается в `header.tsx` через `next/dynamic` с `ssr: false`.
- Sheet в мобильном меню содержит `SheetTitle` с `sr-only`.
