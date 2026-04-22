# Задача 25 — Автотесты: план

## Цель

Подключить Vitest + Testing Library + MSW; покрыть ключевые UI-компоненты и формы; цель `make frontend-test` выполняется.

## Состав работ

1. Dev-зависимости: `vitest`, `@testing-library/react`, `@testing-library/user-event`, `@testing-library/jest-dom`, `msw`, `@vitejs/plugin-react`, `jsdom`.
2. `vitest.config.ts` — `jsdom`, алиас `@/*`, `NEXT_PUBLIC_API_URL` для MSW.
3. `src/test/setup.ts` — `jest-dom`, MSW `setupServer` (GET/PUT `/v1/settings`, POST `/v1/auth/login`), мок `next/link`.
4. Unit: `LessonCard`, `StudentCard`, `ThemeToggle`.
5. Integration: `LoginForm` (мок `loginAction`), `SettingsForm` (реальный `updateSettingsAction` + MSW + моки `next/headers`, `next/cache`, `sonner`).
6. `package.json` — `"test": "vitest run"`.

## Артефакты

См. [summary.md](./summary.md).
