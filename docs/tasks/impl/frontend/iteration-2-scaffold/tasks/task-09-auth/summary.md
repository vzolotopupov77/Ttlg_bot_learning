# Задача 09 — Форма входа и защищённые роуты: summary

## Статус

✅ Done

## Результат

- Страница `src/app/(auth)/login/` с клиентской формой (`login-form.tsx`): FieldGroup/Field, Server Action `loginAction`, cookie `ttlg_access_token` из ответа backend.
- `src/lib/auth.ts`: `getSession`, `getUser` с `React.cache()`.
- `src/middleware.ts`: редирект неаутентифицированных на `/login`; при отсутствии `AUTH_SECRET` редирект на `/login` (конфигурация).
- `src/app/api/auth/logout/route.ts`: `POST`, очистка cookie.

## Заметки

- Для проверки JWT в middleware в `.env.local` нужен `AUTH_SECRET` = `SECRET_KEY` backend.
- Роль в middleware берётся из payload JWT (`role`).
