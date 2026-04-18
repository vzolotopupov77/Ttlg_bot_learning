# Задача 20 — Лента диалога

## Что меняется

- `frontend/src/components/student-dialogue-feed.tsx` — клиентский компонент, `IntersectionObserver`, пагинация `limit`/`offset`.

## API

- `GET /v1/students/{id}/dialogue`

## Критерии

- Различие user/assistant; подгрузка при скролле вверх.
