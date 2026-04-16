# Задача 07 — Инициализация Next.js: summary

## Статус

✅ Done

## Результат

- Создан `frontend/` через `create-next-app` (App Router, `src/`, TypeScript, Tailwind, ESLint).
- Добавлен корневой `pnpm-workspace.yaml` с пакетом `frontend`.
- Выполнен `shadcn init` (preset `base-nova`, `components.json`, `src/lib/utils.ts`, базовые компоненты).
- Корневой `layout.tsx` обновлён с `Providers` и `suppressHydrationWarning`; добавлены `not-found.tsx`, `app/page.tsx`.

## Заметки

- Удалён ошибочно созданный в `frontend/` файл `pnpm-workspace.yaml` (конфиг только в корне репозитория).
