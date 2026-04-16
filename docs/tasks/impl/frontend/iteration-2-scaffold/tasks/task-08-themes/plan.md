# Задача 08 — Темы (light/dark): план

## Цель

Настроить light/dark темы через `next-themes` и CSS-переменные shadcn. Пользователь переключает тему кнопкой; выбор сохраняется без мигания при перезагрузке (FOUC отсутствует).

## Что меняется

| Файл | Тип изменения | Описание |
|------|---------------|----------|
| `frontend/src/app/globals.css` | изменение | Только семантические CSS-переменные shadcn для light/dark |
| `frontend/src/app/layout.tsx` | изменение | `<html suppressHydrationWarning>` (уже из задачи 07); ничего не добавляется |
| `frontend/src/components/providers.tsx` | изменение | Добавить `ThemeProvider` из `next-themes` |
| `frontend/src/components/theme-toggle.tsx` | **новый** | Client Component с кнопкой переключения |

## Зависимости задачи

- Задача 07 выполнена: `frontend/` существует, shadcn инициализирован, `providers.tsx` создан.
- Из `components.json` получено `iconLibrary` (lucide / radix-icons) — использовать нужный пакет иконок.

## Пошаговый план реализации

### 1. Установка next-themes

```bash
pnpm --filter frontend add next-themes
```

### 2. ThemeProvider в providers.tsx

```tsx
"use client"

import { ThemeProvider } from "next-themes"

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </ThemeProvider>
  )
}
```

`disableTransitionOnChange` — предотвращает мигание CSS-анимаций при смене темы.

### 3. CSS-переменные в globals.css

Удалить все raw-цвета (`bg-blue-*`, `gray-*`) из `globals.css`. Оставить **только семантические токены shadcn**:

```css
@layer base {
  :root {
    --background: ...;
    --foreground: ...;
    --primary: ...;
    --primary-foreground: ...;
    /* ... остальные shadcn-токены ... */
    --radius: 0.5rem;
  }
  .dark {
    --background: ...;
    --foreground: ...;
    /* ... dark-значения ... */
  }
}
```

> Конкретные значения берутся из вывода `shadcn init` или из официальной темы shadcn. Не менять вручную без необходимости.

Правила:
- Нет `bg-blue-500`, `text-gray-900` и т.п. в `globals.css`
- Нет ручных `dark:bg-*` — тема управляется только через переменные и класс `.dark` на `<html>`

### 4. ThemeToggle компонент

`frontend/src/components/theme-toggle.tsx`:

```tsx
"use client"

import { Moon, Sun } from "lucide-react"  // или иконки из iconLibrary
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      aria-label="Переключить тему"
    >
      <Sun className="size-4 rotate-0 scale-100 transition-transform dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute size-4 rotate-90 scale-0 transition-transform dark:rotate-0 dark:scale-100" />
    </Button>
  )
}
```

> Если `iconLibrary` в `components.json` — `radix-icons`, использовать `@radix-ui/react-icons` вместо `lucide-react`.

### 5. Проверка

- `pnpm --filter frontend dev` → открыть `http://localhost:3000`
- Нажать `ThemeToggle` → класс `dark` добавляется на `<html>`
- Обновить страницу → тема сохранена (нет FOUC)
- Проверить DevTools: нет ошибок hydration

## Запреты

- Не создавать отдельный CSS-файл для темы — только `globals.css` (правило `tailwindCssFile`).
- Не добавлять ручные `dark:text-*` / `dark:bg-*` в компоненты — только через CSS-переменные.
- `ThemeProvider` не переносить в `layout.tsx` — остаётся в `providers.tsx`.

## Definition of Done

- [ ] `ThemeToggle` переключает классы `light`/`dark` на `<html>`
- [ ] CSS-переменные shadcn применяются в обеих темах — нет raw-цветов в `globals.css`
- [ ] Выбор темы сохраняется в `localStorage`; FOUC отсутствует
- [ ] `ThemeProvider` изолирован в `providers.tsx`, `layout.tsx` — Server Component
- [ ] Нет TypeScript-ошибок
