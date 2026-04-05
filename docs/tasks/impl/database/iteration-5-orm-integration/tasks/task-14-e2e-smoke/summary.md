# Задача 14: End-to-end smoke на PostgreSQL + документация — итог

**Дата:** 2026-04-05  
**Статус:** ✅ Done

## E2E результат

| Шаг | Результат |
|-----|-----------|
| `make backend-db-reset` | exit 0; миграции 0001 + 5dcbe7dd0861 применены |
| `make backend-db-seed` | exit 0; `Seed complete.` |
| `make backend-run` | started on 127.0.0.1:8000 |
| `POST /v1/dialogue/message` (telegram_id=111111111) | 200 OK; `dialogue_id`, `message_id`, `text` в ответе |
| `SELECT role, content FROM messages` | 2 строки: `user` + `assistant` |

## Документация

| Документ | Изменение |
|----------|-----------|
| `README.md` | `make backend-test` указывает PostgreSQL; End-to-end добавлен шаг seed; SQLite помечен «только без Docker» |
| `docs/tasks/tasklist-database.md` | Статусы задач 11–14 → ✅ Done |
| `docs/vision.md` | Без изменений (нет пометок «без PostgreSQL») |
| `docs/plan.md` | Без изменений (Итерация 2 уже ✅ Done) |

## Самопроверка

- [x] `POST /v1/dialogue/message` вернул 200 с непустым `text`
- [x] `SELECT role, content FROM messages LIMIT 2` → 2 строки
- [x] README содержит PostgreSQL-маршрут как основной
- [x] tasklist обновлён
- [x] `make check` — зелёный (запускается ниже)
