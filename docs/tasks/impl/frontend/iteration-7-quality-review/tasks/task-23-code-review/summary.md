# Задача 23 — Ревью кода и тема по макетам: summary

## Дата завершения

2026-04-21

## Что сделано

### Server/Client-граница

- Все `page.tsx` — Server Components (grep `"use client"` в page.tsx — пусто).
- Ни один `page.tsx` не содержит `useState`, `useEffect`, `useRef`.
- Данные во всех страницах тянутся через `lib/api-server.ts` + `lib/auth.ts` на сервере.
- Параллельные фетчи через `Promise.all` реализованы в двух ключевых страницах:
  - `teacher/calendar/page.tsx` — 6 независимых запросов параллельно.
  - `teacher/students/[id]/page.tsx` — 4 независимых запроса параллельно.

### Миграция middleware → proxy (Next.js 16)

- `src/middleware.ts` переименован в `src/proxy.ts`, функция `middleware` → `proxy`.
- Устранено deprecation-предупреждение сборки.
- Сборка с `pnpm --filter frontend build` чистая (нет предупреждений и TS-ошибок).

### Исправлен raw-цвет

- `components/student-stats.tsx`: `text-green-600 dark:text-green-500` заменён на `text-success`.
- Добавлен семантический токен `--success` / `--success-foreground` в `globals.css` и `@theme inline`.

### Loading / Error

- `loading.tsx` присутствует для всех 5 ключевых роутов (было готово с предыдущих итераций):
  - `(app)/teacher/calendar/loading.tsx`
  - `(app)/teacher/settings/loading.tsx`
  - `(app)/teacher/students/loading.tsx`
  - `(app)/teacher/students/[id]/loading.tsx`
  - `(app)/student/schedule/loading.tsx`
- `(app)/error.tsx` присутствует на уровне группы.

### Палитра темы (Вариант B — Violet)

Источник: lovable.app-дизайн для tutor-schedule приложений (EdTech, violet-акцент).

Обновлён `frontend/src/app/globals.css`:

| Токен | `:root` | `.dark` |
|---|---|---|
| `--primary` | `oklch(0.50 0.24 285)` — насыщенный фиолетовый | `oklch(0.68 0.20 285)` — светлее для тёмного фона |
| `--primary-foreground` | `oklch(0.99 0 0)` белый | `oklch(0.12 0 0)` почти чёрный |
| `--ring` | `oklch(0.50 0.24 285)` | `oklch(0.68 0.20 285)` |
| `--accent` | `oklch(0.93 0.05 285)` лавандовый оттенок | `oklch(0.27 0.07 285)` тёмный фиолетовый |
| `--accent-foreground` | `oklch(0.35 0.18 285)` | `oklch(0.85 0.10 285)` |
| `--success` | `oklch(0.53 0.15 145)` зелёный | `oklch(0.64 0.15 145)` |
| `--sidebar-primary` | `oklch(0.50 0.24 285)` | `oklch(0.68 0.20 285)` |
| `chart-1..5` | градиент фиолетового (L: 0.50→0.93) | градиент (L: 0.68→0.36) |

Фоны, карточки, бордюры, muted — нейтральные (без хроматики) — без изменений.

## Найденные замечания (не критические, зафиксированы)

- `space-y-*` / `space-x-*` используются в ряде компонентов (`lesson-card`, `weekly-schedule`, `student-card` и др.) — shadcn рекомендует `flex gap-*`, но функционально это не баг; массовый рефакторинг отложен.
- В `(app)/layout.tsx` — отдельных `error.tsx` на уровне каждого сегмента нет; общий `(app)/error.tsx` покрывает все роуты — для текущего масштаба приложения достаточно.

## Definition of Done

**Агент:**

- [x] Все Server Components не импортируют клиентские хуки или browser API
- [x] `pnpm --filter frontend build` — нет TypeScript/ESLint ошибок и предупреждений сборки
- [x] `loading.tsx` присутствует для всех 5 основных роутов
- [x] Критические находки исправлены (`middleware→proxy`, `text-green-600→text-success`)
- [x] Палитра из макетов отражена в теме (`globals.css`); новые цвета не вводятся через raw Tailwind-классы

**Пользователь:**

- [ ] Запустить `make frontend-build` — сборка проходит без ошибок
- [ ] Открыть `/teacher/calendar` с медленной сетью (DevTools Throttling) — видна skeleton/loading UI
- [ ] Визуально сверить акцент кнопок/полей с макетами (violet primary) в light и dark
