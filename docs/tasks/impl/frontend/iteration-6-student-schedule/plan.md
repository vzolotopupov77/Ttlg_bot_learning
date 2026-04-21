# Итерация 6 — Расписание ученика

**Статус:** ✅ закрыта — реализация **2026-04-21**, ручная приёмка подтверждена; дополнение **2026-04-22** — Alembic `env.py` и проверка пароля ученика; см. [summary.md](summary.md).

## Цель

Экран `/student/schedule`: недельная сетка занятий (`GET /v1/student/schedule`), навигация по неделям, детали занятия в `Sheet`, без кнопки добавления занятий. Соответствует [frontend-requirements.md](../../../../spec/frontend-requirements.md) (экран 5): только **недельный** вид; месячный — вне scope.

## Состав работ (задача 22)

| Задача | Содержание |
|--------|------------|
| 22 | `StudentScheduleView`, доработка `WeeklySchedule` / `LessonCard`, миграция пароля тестового ученика |

## Технические ориентиры

- API: [api-contracts.md](../../../../tech/api-contracts.md) — `GET /v1/student/schedule`.
- Тестовый вход ученика: миграция `e1f2a3b4c5d6`, `STUDENT_DEFAULT_PASSWORD` в `.env.example`; загрузка `.env` для Alembic — `backend/alembic/env.py`.

## Критерии завершения

- [x] Код и артефакты — в [summary.md](summary.md)
- [x] Самопроверки агента — в [summary.md](summary.md)
- [x] Ручная приёмка — [summary.md](summary.md)
