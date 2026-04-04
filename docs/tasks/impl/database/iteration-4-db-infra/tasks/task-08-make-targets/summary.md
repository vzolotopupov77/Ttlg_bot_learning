# Задача 08 — Недостающие make-цели: summary

**Дата:** 2026-04-04  
**Статус:** ✅ Done

## Что сделано

- Добавлены 3 цели в `Makefile`: `backend-db-reset`, `backend-db-shell`, `backend-db-logs`
- Добавлена цель `backend-db-seed` (из задачи 09) — внесена сразу в `.PHONY` вместе с остальными
- Обновлён `.PHONY`: все 4 новые цели
- Добавлен `backend/scripts` в пути `lint` и `format` (обнаружено при реализации задачи 09)
- Обновлён `docs/tech/db-guide.md` раздел 2: заглушка «добавится в итерации 4» заменена актуальной таблицей

## Реализация

`backend-db-reset` выполняет три шага последовательно:
1. `docker compose down -v` — удаляет контейнер и volume `ttlg_pg_data`
2. `docker compose up -d --wait db` — ждёт healthcheck (`pg_isready`)
3. `alembic upgrade head` — накатывает миграции

`backend-db-shell` и `backend-db-logs` — однострочные обёртки над `docker compose exec`/`logs`.

## Отклонения от плана

Нет.

## Проверка

- `make backend-db-reset` — завершился без ошибок; миграция `0001_initial_schema` применена
- `make backend-db-shell` + `\dt` — 7 строк (6 таблиц схемы + `alembic_version`)
- `make lint` — `All checks passed!`
