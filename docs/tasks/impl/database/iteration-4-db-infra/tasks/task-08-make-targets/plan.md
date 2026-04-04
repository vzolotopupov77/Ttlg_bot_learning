# Задача 08 — Недостающие make-цели: план

**Итерация:** 4  
**Дата:** 2026-04-04  
**Статус:** In Progress

## Цель

Добавить в `Makefile` три цели для полного цикла локальной работы с БД: пересоздание окружения, интерактивный шелл, просмотр логов контейнера.

## Затрагиваемые файлы

| Файл | Изменение |
|------|-----------|
| `Makefile` | Добавить 3 цели + расширить `.PHONY` |
| `docs/tech/db-guide.md` | Обновить раздел 2 «Makefile-цели» — убрать заглушку, добавить три новые |

## Реализация

### Makefile

```makefile
backend-db-reset:
	docker compose down -v
	docker compose up -d --wait db
	uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

backend-db-shell:
	docker compose exec db psql -U ttlg -d ttlg

backend-db-logs:
	docker compose logs -f db
```

Детали:
- `down -v` — останавливает контейнер и удаляет volume `ttlg_pg_data`
- `up -d --wait` — ждёт прохождения healthcheck (`pg_isready`) до запуска миграций
- реквизиты psql берутся из `docker-compose.yml`: `-U ttlg -d ttlg`

### `.PHONY`

Добавить в строку `.PHONY`: `backend-db-reset backend-db-shell backend-db-logs` (и `backend-db-seed` из задачи 09).

## Самопроверка

- `make backend-db-reset` завершается без ошибок (down → up → migrate)
- После reset: `make backend-db-migrate` → `Already at head`
- `make backend-db-shell` → открывается `psql`; `\dt` показывает 6 таблиц
- `make backend-db-logs` → в выводе `database system is ready to accept connections`
- Все цели присутствуют в `.PHONY`
- В `db-guide.md` нет заглушки «добавится в итерации 4»
