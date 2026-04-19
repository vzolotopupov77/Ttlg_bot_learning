# Итерация 5 — Экран Настройки системы

**Статус:** ✅ Закрыта — см. [summary.md](summary.md) (реализация и приёмка **2026-04-19**).

## Цель

Реализовать `/teacher/settings` с формой системных настроек преподавателя и сохранением через `GET`/`PUT /v1/settings`.

## Состав работ (задача 21)

| Задача | Содержание |
|--------|------------|
| 21 | Форма: react-hook-form + zod, две карточки, загрузка на сервере, сохранение через Server Action |

## Технические ориентиры

- API: [api-contracts.md](../../../../tech/api-contracts.md) — раздел «Настройки системы».
- Требования UI: [frontend-requirements.md](../../../../spec/frontend-requirements.md) — экран 4.

## Критерии завершения

- [x] Задача 21 реализована; артефакты перечислены в [summary.md](summary.md)
- [x] `make frontend-lint` / `make frontend-build` — см. самопроверки в [summary.md](summary.md)
- [x] Ручная приёмка по чек-листу в [summary.md](summary.md) (**2026-04-19**; без отдельной проверки skeleton при throttling)

## Прогресс

Сводная таблица статусов — в [summary.md](summary.md), раздел **«Прогресс итерации (сводка)»**. Строка в [tasklist-frontend.md](../../tasklist-frontend.md) (таблица «Прогресс», итерация 5) синхронизирована с закрытием.
