# Задача 11 — Маршрутизация и Makefile: summary

## Статус

✅ Done

## Результат

- Заглушки страниц: `teacher/calendar`, `teacher/students`, `teacher/settings`, `student/schedule` + соответствующие `loading.tsx` с `Skeleton`.
- Middleware дополнен блокировкой `teacher`/`student` для чужих префиксов путей; редирект с `/` и `/login` при наличии валидной сессии.
- Корневой `Makefile`: цели `frontend-dev`, `frontend-build`, `frontend-lint`, `frontend-test`; `check` включает `frontend-lint`.
- В `frontend/package.json` скрипт `test` — заглушка до итерации 8.
