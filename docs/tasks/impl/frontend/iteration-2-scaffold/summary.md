# Итерация 2 — Каркас frontend: summary

## Статус

✅ Завершена (реализация по плану итерации).

## Что сделано

- Создан монорепо-фрагмент: корневой `pnpm-workspace.yaml`, пакет `frontend/` (Next.js 16 App Router, TypeScript, Tailwind CSS v4, ESLint).
- Инициализирован **shadcn/ui** (preset `base-nova`, `components.json`, семантические токены в `globals.css`).
- Подключены **темы**: `next-themes`, `ThemeProvider` в `providers.tsx`, `ThemeToggle`, `suppressHydrationWarning` на `<html>`.
- **Аутентификация**: форма `/login` (Server Action `loginAction`), копирование JWT из `Set-Cookie` backend в httpOnly cookie `ttlg_access_token`; `getUser`/`getSession` с `React.cache()`; `POST /api/auth/logout`.
- **Middleware** (`jose`): проверка JWT, редиректы по ролям, блокировка перекрёстного доступа `teacher` ↔ `student`; требуется `AUTH_SECRET` = `SECRET_KEY` backend.
- **Layout**: `Sidebar`, `Header`, `MobileNav` (Sheet + `SheetTitle`), ленивая загрузка мобильного меню через `next/dynamic`.
- **Роуты-заглушки** с `loading.tsx` (Skeleton): `/teacher/calendar`, `/teacher/students`, `/teacher/settings`, `/student/schedule`.
- **Makefile**: `frontend-dev`, `frontend-build`, `frontend-lint`, `frontend-test`; цель `check` дополнена `frontend-lint`.
- Артефакт **`frontend/.env.local.example`**: `NEXT_PUBLIC_API_URL`, `AUTH_SECRET`, `NEXT_PUBLIC_SITE_URL`.

## Отклонения и решения

- **Cookie**: имя `ttlg_access_token` взято из backend (`ACCESS_TOKEN_COOKIE`), не абстрактное `token`.
- **SheetTrigger** (Base UI): вместо `asChild` используется проп `render` с `Button` и иконкой внутри.
- **Next.js 16**: предупреждение о переименовании middleware → proxy — пока оставлен классический `middleware.ts` по плану итерации.
- Вложенный `frontend/pnpm-workspace.yaml` от `create-next-app` удалён; workspace только в корне репозитория.

## Проверки

### Автоматические (зафиксировано при приёмке)

| Команда | Результат | Примечание |
|---------|-----------|------------|
| `pnpm --filter frontend lint` | Успех | ESLint без ошибок |
| `pnpm --filter frontend build` | Успех | Next.js 16.2.3, TypeScript; предупреждение о депрекации `middleware` → `proxy` (ожидаемо, см. выше) |

Окружение сборки: использован `frontend/.env.local` с `AUTH_SECRET`, согласованным с backend.

### Ручной смоук (оператор, после чек-листа)

Проверено: запуск backend + `make frontend-dev`; `AUTH_SECRET` = `SECRET_KEY`; логин преподавателя → `/teacher/calendar`; httpOnly cookie; блокировка перекрёстного доступа teacher/student; переключение темы и мобильный drawer; выход на `/login`. Результат: **ок**.

### Наблюдение по UI

Внешний вид в **нейтральной палитре** (почти монохром, акцент по умолчанию у `destructive`) — ожидаемо для `components.json` → `baseColor: "neutral"` и семантических токенов без отдельного бренд-акцента в `globals.css`. Смена акцента — отдельная настройка, не дефект итерации 2.

## Что сделать локально перед `make frontend-dev`

1. Скопировать `frontend/.env.local.example` → `frontend/.env.local`.
2. Выставить **`AUTH_SECRET`** равным **`SECRET_KEY`** из backend `.env`.
3. При необходимости поправить `NEXT_PUBLIC_API_URL` (по умолчанию `http://127.0.0.1:8000`).
4. Backend запущен (`make backend-run`), БД доступна.
