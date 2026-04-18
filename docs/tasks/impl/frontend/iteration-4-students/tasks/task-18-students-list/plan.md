# Задача 18 — Список учеников

## Что меняется

- Страница `frontend/src/app/(app)/teacher/students/page.tsx` — загрузка списка, клиентский вид с переключателем `?view=cards|table`.
- Компоненты: `student-card`, `student-table`, `student-dialog`.
- Server actions: `frontend/src/app/actions/students.ts`.

## Файлы

- `page.tsx`, `students-view.tsx` (или встроенный клиент в page — по реализации)
- `student-card.tsx`, `student-table.tsx`, `student-dialog.tsx`
- `actions/students.ts`

## Критерии

- CRUD через API; список обновляется после операций; форма с полями профиля, включая **Telegram ID** (`telegram_id` в API), и `notes`.
