# Задача 02 — API-контракты для frontend: summary

## Статус

✅ Завершена.

## Что сделано

- В [`docs/tech/api-contracts.md`](../../../../../../tech/api-contracts.md) добавлен раздел **«API для frontend (проект)»**:
  - аутентификация: `POST /v1/auth/login` (поля `email`, `password`, `role`), `POST /v1/auth/logout`, `GET /v1/auth/me`;
  - преподаватель: `GET /v1/teacher/schedule`, bot-requests, unconfirmed-lessons, pending-homework, напоминания, reschedule-requests;
  - ученики (CRUD): `/v1/students`, в т.ч. `notes` и **`telegram_id`** в теле запроса/ответа; опционально `GET .../stats` или агрегаты в профиле;
  - занятия: `PUT`, `DELETE`, `PATCH .../flags` (немедленное обновление флагов);
  - настройки: `GET`/`PUT /v1/settings`;
  - ученик: `GET /v1/student/schedule?week_start=`.
- Зафиксированы общие правила: httpOnly cookie, формат ошибок из [api-conventions.md](../../../../../../api-conventions.md), пагинация списков.
- Дублирования с таблицей MVP в начале файла нет; явное расширение CRUD занятий.

## Проверка по api-design-principles

- Ресурсы во мн.ч. (`/students`, `/teacher/...`), семантика HTTP-методов соблюдена.
- Списки с `items` + `total` + `limit` + `offset`.
- Полный отчёт и дополнения к контракту (таблица соответствия, RPC-напоминания, query для списка учеников, `409`, тела `remind-*`, обёртка расписания) — в [`docs/tech/api-contracts.md`](../../../../../../tech/api-contracts.md), подраздел **«Проверка по api-design-principles»** (после блока «API для frontend»).

## Отклонения от черновика плана задачи 02

- ~~Вход: `login` вместо e-mail~~ — **зафиксировано:** в теле запроса поле **`email`** (логин = e-mail).
- Расписание ученика: вместо только `GET /v1/students/{id}/schedule?month=` добавлен **`GET /v1/student/schedule?week_start=`** для текущего пользователя; недельный параметр согласован с календарём преподавателя.

## Проблемы

Не выявлено.

## Пользователь (DoD)

- [x] Проверка раздела «API для frontend» в `docs/tech/api-contracts.md` и покрытия экранов — выполнено (зафиксировано в `tasklist-frontend.md`).

## Сводка итерации

Итоговый документ по итерации 0: [../../summary.md](../../summary.md).
