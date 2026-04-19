# Задача 21 — Форма настроек системы

**Итерация:** 5  
**Статус:** ✅ Закрыта — см. [summary.md](summary.md) (приёмка **2026-04-19**).

## Цель

Страница `/teacher/settings` с полями из контракта `GET`/`PUT /v1/settings`, валидацией и кнопками «Сохранить» / «Сбросить».

## Артефакты

- [`frontend/src/app/(app)/teacher/settings/page.tsx`](../../../../../../../frontend/src/app/(app)/teacher/settings/page.tsx)
- [`frontend/src/app/(app)/teacher/settings/loading.tsx`](../../../../../../../frontend/src/app/(app)/teacher/settings/loading.tsx)
- [`frontend/src/components/settings-form.tsx`](../../../../../../../frontend/src/components/settings-form.tsx)
- [`frontend/src/lib/types/settings.ts`](../../../../../../../frontend/src/lib/types/settings.ts)
- [`frontend/src/lib/api-server.ts`](../../../../../../../frontend/src/lib/api-server.ts) — `fetchSettings()`
- [`frontend/src/app/actions/settings.ts`](../../../../../../../frontend/src/app/actions/settings.ts) — `updateSettingsAction`
