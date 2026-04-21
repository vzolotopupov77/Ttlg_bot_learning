# Задача 22 — Календарь расписания ученика

**Итерация:** 6  
**Статус:** ✅ закрыта — реализация **2026-04-21**, приёмка подтверждена; см. [summary.md](summary.md).

## Цель

Страница `/student/schedule`: недельное расписание по [frontend-requirements.md](../../../../../spec/frontend-requirements.md) (экран 5): только недельный вид; месячный — не реализован (вне спецификации).

## Артефакты

- [`frontend/src/app/(app)/student/schedule/page.tsx`](../../../../../../../frontend/src/app/(app)/student/schedule/page.tsx)
- [`frontend/src/components/student-schedule-view.tsx`](../../../../../../../frontend/src/components/student-schedule-view.tsx)
- [`frontend/src/lib/api-server.ts`](../../../../../../../frontend/src/lib/api-server.ts) — `fetchStudentSchedule`
- [`frontend/src/components/weekly-schedule.tsx`](../../../../../../../frontend/src/components/weekly-schedule.tsx)
- [`frontend/src/components/lesson-card.tsx`](../../../../../../../frontend/src/components/lesson-card.tsx)
- [`backend/alembic/versions/e1f2a3b4c5d6_seed_student_web_password.py`](../../../../../../../backend/alembic/versions/e1f2a3b4c5d6_seed_student_web_password.py)
- [`backend/alembic/env.py`](../../../../../../../backend/alembic/env.py) — явная загрузка корневого `.env` для миграций
- [`.env.example`](../../../../../../../.env.example) — `STUDENT_DEFAULT_PASSWORD`
