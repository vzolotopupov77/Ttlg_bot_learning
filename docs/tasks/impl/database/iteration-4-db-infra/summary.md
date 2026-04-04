# Итерация 4 — Инфраструктура БД: summary

**Дата:** 2026-04-04  
**Статус:** ✅ Done

## Что сделано

| Задача | Артефакты |
|--------|-----------|
| 08 — Makefile-цели | `Makefile`: +4 цели, расширен `.PHONY`, `lint`/`format` покрывают `backend/scripts` |
| 09 — Seed-скрипт | `backend/scripts/seed.py`, цель `backend-db-seed` |
| 10 — Инспекция | `db-guide.md`: раздел 5 без заглушек, новый раздел 6 «Просмотр данных» |

## Новые Makefile-цели

```bash
make backend-db-reset   # чистый старт: down -v → up --wait → migrate
make backend-db-shell   # psql -U ttlg -d ttlg
make backend-db-logs    # docker compose logs -f db
make backend-db-seed    # python backend/scripts/seed.py (идемпотентно)
```

## Seed-данные

- teacher: `Преподаватель` (role=teacher)
- student: `Ученик` (role=student, telegram_id=`111111111`)
- lesson: `Seed-занятие` (scheduled, завтра)
- assignment: `Seed-задание` (pending, через 7 дней)

## Проверка итерации

**Агент (автоматически):**
```
make backend-db-reset     → exit 0; миграции применены
make backend-db-seed      → exit 0; Seed complete.
make backend-db-shell     → \dt: 7 строк (6 схема + alembic_version)
                          → SELECT name, role FROM users ORDER BY role: 2 строки
make lint                 → All checks passed!
```

**Пользователь (ручная проверка, 2026-04-04):** ✅ Пройдено
```
make backend-db-reset
make backend-db-migrate
make backend-db-seed
make backend-db-shell → \dt → таблицы видны
                      → SELECT name, role FROM users; → 2 строки
```

## Отклонения

- `backend/scripts` добавлен в `lint` и `format` — обнаружено при написании скрипта.
- Раздел 6 `db-guide.md` включает блок запросов с `telegram_id` вместо UUID — удобнее для ручного использования.
