# Задача 19 — Детальная страница ученика

## Что меняется

- `frontend/src/app/(app)/teacher/students/[id]/page.tsx`
- `student-stats.tsx`, `student-lessons-history.tsx`

## API

- `GET /v1/students/{id}`, `GET /v1/students/{id}/lessons`, `GET /v1/students/{id}/stats`

## Критерии

- Профиль, метрики, таблица занятий с теми же 5 флагами, что в календаре.
