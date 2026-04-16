# Задача 07 — Инициализация проекта Next.js: план

## Цель

Создать `frontend/` с настроенным стеком (Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui) и подключить его в монорепо через `pnpm-workspace.yaml`. Проект должен запускаться и успешно собираться.

## Что меняется

### Новые файлы

| Файл/директория | Описание |
|-----------------|----------|
| `pnpm-workspace.yaml` | Корневой файл монорепо: `packages: ["frontend"]` |
| `frontend/` | Next.js-проект (генерируется `create-next-app`) |
| `frontend/components.json` | Конфиг shadcn/ui (генерируется `shadcn init`) |
| `frontend/.env.local.example` | Переменная `NEXT_PUBLIC_API_URL=http://localhost:8000` |
| `frontend/src/app/layout.tsx` | Корневой layout: `metadata` export, `<html suppressHydrationWarning>`, `<Providers>` |
| `frontend/src/app/not-found.tsx` | Страница 404 (файловая конвенция App Router) |
| `frontend/src/components/providers.tsx` | Client Component-обёртка провайдеров (`"use client"`) |

### Изменяемые файлы

Нет — задача только создаёт новые сущности.

## Пошаговый план реализации

### 1. pnpm-workspace.yaml

Создать в корне репозитория:

```yaml
packages:
  - "frontend"
```

### 2. Инициализация Next.js

```bash
pnpm create next-app frontend --typescript --tailwind --app --src-dir --no-git --import-alias "@/*"
```

Ключевые флаги:
- `--app` — App Router
- `--src-dir` — исходники в `src/`
- `--no-git` — не создавать отдельный `.gitignore` внутри (корневой репо)
- `--import-alias "@/*"` — алиас для импортов

### 3. Инициализация shadcn/ui

```bash
pnpm --filter frontend dlx shadcn@latest init
```

При интерактивном вопросе выбрать: стиль **Default**, базовый цвет **Slate** (или предложенный для Tailwind v4), путь к CSS — `src/app/globals.css`.

После init выполнить аудит `components.json`:
- `tailwindVersion` должен быть `"4"` (если CLI поддерживает) или `"3"`
- `aliases.components` → `"@/components"`
- `aliases.utils` → `"@/lib/utils"`
- `rsc: true` — обязателен для App Router

Зафиксировать `isRSC`, `base`, `iconLibrary` в summary для использования в задачах 08–11.

### 4. Добавление базовых shadcn-компонентов

```bash
pnpm --filter frontend dlx shadcn@latest add button input card dialog sheet badge separator label switch skeleton alert
```

После установки прочитать добавленные файлы в `src/components/ui/` — проверить корректность импортов (`cn`, `cva`, иконки).

> Компонент `empty` может отсутствовать в shadcn — при ошибке пропустить, создать вручную как простой placeholder в задаче 10.

### 5. Настройка корневого layout

`frontend/src/app/layout.tsx` — Server Component:

```tsx
import type { Metadata } from "next"
import { Providers } from "@/components/providers"
import "./globals.css"

export const metadata: Metadata = {
  title: "Репетитор",
  description: "Система управления занятиями",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

`frontend/src/components/providers.tsx` — Client Component (пока пустой, ThemeProvider добавляется в задаче 08):

```tsx
"use client"

export function Providers({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}
```

### 6. not-found.tsx

`frontend/src/app/not-found.tsx` — минимальная страница 404.

### 7. .env.local.example

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 8. Проверка

```bash
pnpm --filter frontend dev     # должен запуститься на :3000
pnpm --filter frontend build   # должен пройти без ошибок
```

## Запреты

- Не создавать `index.ts` barrel-файлы в `src/` (правило `bundle-barrel-imports`).
- Не добавлять `"use client"` в `layout.tsx` — он должен оставаться Server Component.
- Не редактировать shadcn-компоненты вручную (только через CLI).

## Риски

| Риск | Митигация |
|------|-----------|
| `shadcn init` может не поддерживать Tailwind v4 | Проверить вывод; если ошибка — использовать `--legacy-peer-deps` или откатиться до Tailwind v3-совместимого пресета |
| `pnpm create next-app` требует интерактивного ввода | Использовать флаги CLI, избегать интерактива |

## Definition of Done

- [ ] `pnpm-workspace.yaml` создан, `frontend` зарегистрирован как пакет
- [ ] `pnpm --filter frontend dev` стартует без ошибок
- [ ] `pnpm --filter frontend build` проходит успешно
- [ ] `components.json` присутствует с корректными `aliases`, `rsc: true`
- [ ] `layout.tsx` содержит `export const metadata`, `<html suppressHydrationWarning>`
- [ ] `not-found.tsx` создан
- [ ] Barrel-файлов в `src/` нет
- [ ] TypeScript-ошибок нет
