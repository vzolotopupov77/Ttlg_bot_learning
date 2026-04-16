# Итерация 3 — Календарь преподавателя

**Статус:** ✅ Завершена (2026-04-16). Задачи 12–17 выполнены; автоматические проверки и ручная приёмка — в [summary.md](summary.md).

## Цель

Реализовать экран `/teacher/calendar`: недельная сетка занятий с CRUD и флагами, четыре нижние панели (бот-лента, переносы, неподтверждённые занятия, несданные ДЗ).

## Ценность

Преподаватель видит расписание на неделю и управляет занятиями без выхода из веб-интерфейса; быстрый обзор активности бота и запросов учеников.

## Состав работ (задачи 12–17)

| Задача | Содержание |
|--------|------------|
| 12 | `WeeklySchedule`, `LessonCard`, данные `GET /v1/teacher/schedule` |
| 13 | `LessonDialog` — CRUD `POST/PUT/DELETE /v1/lessons`, `PATCH .../flags` |
| 14 | `BotRequestsFeed` — `GET /v1/teacher/bot-requests` |
| 15 | `UnconfirmedLessons` + `POST .../remind-unconfirmed` |
| 16 | `PendingHomework` + `POST .../remind-pending-homework` |
| 17 | `RescheduleRequests` + `PATCH .../reschedule-requests/{id}` |

## Технические ориентиры

- API-клиент: `credentials: 'include'`, базовый URL `NEXT_PUBLIC_API_URL`.
- Неделя в query `week_start=YYYY-MM-DD` (понедельник).
- Флаги — optimistic update + `PATCH /v1/lessons/{id}/flags`.
- Toast — Sonner.

## Связанные документы

- [frontend-requirements.md](../../../../spec/frontend-requirements.md) — Экран 2
- [api-contracts.md](../../../../tech/api-contracts.md) — раздел «API для frontend»

## Критерии завершения (зафиксировано)

- [x] Задачи 12–17 закрыты в [tasklist-frontend.md](../../../tasklist-frontend.md)
- [x] `pnpm exec tsc --noEmit`, сборка frontend — без ошибок (см. summary)
- [x] Ручная приёмка сценариев календаря и панелей — см. раздел «Проверки» в [summary.md](summary.md)
