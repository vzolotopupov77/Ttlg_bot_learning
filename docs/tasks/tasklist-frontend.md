# Frontend Tasklist

## Обзор

**Frontend** — веб-приложение на Next.js (App Router) + TypeScript + shadcn/ui + Tailwind CSS. Покрывает два клиентских профиля: **Преподаватель** (управление расписанием, учениками, настройками) и **Ученик** (просмотр расписания). Этот тасклист описывает весь путь: от фиксации требований и проектирования API до каркаса, реализации экранов, ревью качества и тестирования.

Стек: Next.js (App Router), React, TypeScript, shadcn/ui, Tailwind CSS, pnpm.
Каталог проекта: `frontend/`.
Документация API: [docs/tech/api-contracts.md](../tech/api-contracts.md).
Модель данных: [docs/data-model.md](../data-model.md).

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

## Связь с plan.md

| Итерация | Содержание |
|----------|------------|
| Итерация 0 | Требования к UI и API-контракты |
| Итерация 1 | Реализация API для frontend (backend) |
| Итерация 2 | Каркас frontend-проекта |
| Итерация 3 | Экран Преподавателя — Календарь |
| Итерация 4 | Экран Ученики |
| Итерация 5 | Экран Настройки системы |
| Итерация 6 | Экран Расписание Ученика |
| Итерация 7 | Ревью качества кода, палитра темы по макетам |
| Итерация 8 | Тестирование |

## Прогресс (актуально на 2026-04-16)

| Итерация | Статус |
|----------|--------|
| 0 — Требования UI и API | ✅ Done |
| 1 — Backend API для frontend | ✅ Done |
| 2 — Каркас frontend | ✅ Done |
| 3 — Календарь преподавателя | ✅ Done — реализация и проверки зафиксированы в [summary итерации 3](impl/frontend/iteration-3-teacher-calendar/summary.md) |
| 4 — Ученики | 📋 Planned (**следующая**) |
| 5 — Настройки | 📋 Planned |
| 6 — Расписание ученика | 📋 Planned |
| 7 — Ревью качества, палитра по макетам | 📋 Planned |
| 8 — Тестирование | 📋 Planned |

**Текущий фокус:** итерация 4 (задачи 18–20).

---

## Сводная таблица задач

| № | Итерация | Описание | Статус | Документы |
|---|----------|----------|--------|-----------|
| 01 | 0 | Функциональные требования к экранам | ✅ Done | [план](impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/plan.md) \| [summary](impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/summary.md) \| [spec](../../spec/frontend-requirements.md) |
| 02 | 0 | API-контракты для frontend; обновить api-contracts.md | ✅ Done | [план](impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/plan.md) \| [summary](impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/summary.md) |
| 03 | 1 | Анализ пробелов схемы данных | ✅ Done | [план](impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/plan.md) \| [summary](impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/summary.md) |
| 04 | 1 | Новые endpoints backend для frontend | ✅ Done | [план](impl/frontend/iteration-1-backend-api/tasks/task-04-new-endpoints/plan.md) \| [summary](impl/frontend/iteration-1-backend-api/tasks/task-04-new-endpoints/summary.md) |
| 05 | 1 | Миграция с mock-данными | ✅ Done | [план](impl/frontend/iteration-1-backend-api/tasks/task-05-mock-migration/plan.md) \| [summary](impl/frontend/iteration-1-backend-api/tasks/task-05-mock-migration/summary.md) |
| 06 | 1 | Миграция: добавить преподавателя в БД | ✅ Done | [план](impl/frontend/iteration-1-backend-api/tasks/task-06-teacher-migration/plan.md) \| [summary](impl/frontend/iteration-1-backend-api/tasks/task-06-teacher-migration/summary.md) |
| 07 | 2 | Инициализация проекта Next.js | ✅ Done | [план](impl/frontend/iteration-2-scaffold/tasks/task-07-project-init/plan.md) \| [summary](impl/frontend/iteration-2-scaffold/tasks/task-07-project-init/summary.md) |
| 08 | 2 | Темы: светлая/тёмная, CSS variables | ✅ Done | [план](impl/frontend/iteration-2-scaffold/tasks/task-08-themes/plan.md) \| [summary](impl/frontend/iteration-2-scaffold/tasks/task-08-themes/summary.md) |
| 09 | 2 | Форма входа и защищённые роуты | ✅ Done | [план](impl/frontend/iteration-2-scaffold/tasks/task-09-auth/plan.md) \| [summary](impl/frontend/iteration-2-scaffold/tasks/task-09-auth/summary.md) |
| 10 | 2 | Общий layout: навигация, header, drawer | ✅ Done | [план](impl/frontend/iteration-2-scaffold/tasks/task-10-layout/plan.md) \| [summary](impl/frontend/iteration-2-scaffold/tasks/task-10-layout/summary.md) |
| 11 | 2 | Маршрутизация по ролям, Makefile-цели | ✅ Done | [план](impl/frontend/iteration-2-scaffold/tasks/task-11-routing-makefile/plan.md) \| [summary](impl/frontend/iteration-2-scaffold/tasks/task-11-routing-makefile/summary.md) |
| 12 | 3 | Недельное расписание: сетка + карточки занятий | ✅ Done | [план](impl/frontend/iteration-3-teacher-calendar/tasks/task-12-weekly-schedule/plan.md) \| [summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-12-weekly-schedule/summary.md) |
| 13 | 3 | Диалог занятия: CRUD, флаги, кнопки действий | ✅ Done | [план](impl/frontend/iteration-3-teacher-calendar/tasks/task-13-lesson-dialog/plan.md) \| [summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-13-lesson-dialog/summary.md) |
| 14 | 3 | Лента последних 10 bot-запросов учеников | ✅ Done | [план](impl/frontend/iteration-3-teacher-calendar/tasks/task-14-bot-feed/plan.md) \| [summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-14-bot-feed/summary.md) |
| 15 | 3 | Блок неподтверждённых занятий (2 дня) + напоминания | ✅ Done | [план](impl/frontend/iteration-3-teacher-calendar/tasks/task-15-unconfirmed-lessons/plan.md) \| [summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-15-unconfirmed-lessons/summary.md) |
| 16 | 3 | Блок несданных ДЗ (2 дня) + напоминания | ✅ Done | [план](impl/frontend/iteration-3-teacher-calendar/tasks/task-16-pending-hw/plan.md) \| [summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-16-pending-hw/summary.md) |
| 17 | 3 | Блок запросов учеников на перенос занятий | ✅ Done | [план](impl/frontend/iteration-3-teacher-calendar/tasks/task-17-reschedule-requests/plan.md) \| [summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-17-reschedule-requests/summary.md) |
| 18 | 4 | Список учеников: карточки/таблица, CRUD | 📋 Planned | [план](impl/frontend/iteration-4-students/tasks/task-18-students-list/plan.md) \| [summary](impl/frontend/iteration-4-students/tasks/task-18-students-list/summary.md) |
| 19 | 4 | Детальная форма ученика: занятия, счётчики, ДЗ | 📋 Planned | [план](impl/frontend/iteration-4-students/tasks/task-19-student-detail/plan.md) \| [summary](impl/frontend/iteration-4-students/tasks/task-19-student-detail/summary.md) |
| 20 | 4 | Лента диалога ученика с ботом в детальной форме | 📋 Planned | [план](impl/frontend/iteration-4-students/tasks/task-20-student-dialogue/plan.md) \| [summary](impl/frontend/iteration-4-students/tasks/task-20-student-dialogue/summary.md) |
| 21 | 5 | Форма настроек системы | 📋 Planned | [план](impl/frontend/iteration-5-settings/tasks/task-21-settings-form/plan.md) \| [summary](impl/frontend/iteration-5-settings/tasks/task-21-settings-form/summary.md) |
| 22 | 6 | Календарь расписания ученика | 📋 Planned | [план](impl/frontend/iteration-6-student-schedule/tasks/task-22-student-calendar/plan.md) \| [summary](impl/frontend/iteration-6-student-schedule/tasks/task-22-student-calendar/summary.md) |
| 23 | 7 | Ревью кода: Server/Client, мемоизация, bundle; тема по макетам (`globals.css`) | 📋 Planned | [план](impl/frontend/iteration-7-quality-review/tasks/task-23-code-review/plan.md) \| [summary](impl/frontend/iteration-7-quality-review/tasks/task-23-code-review/summary.md) |
| 24 | 8 | Тест-сценарии для 5 экранов (ручные чек-листы) | 📋 Planned | [план](impl/frontend/iteration-8-testing/tasks/task-24-test-scenarios/plan.md) \| [summary](impl/frontend/iteration-8-testing/tasks/task-24-test-scenarios/summary.md) |
| 25 | 8 | Автотесты: unit + integration; `make frontend-test` | 📋 Planned | [план](impl/frontend/iteration-8-testing/tasks/task-25-automated-tests/plan.md) \| [summary](impl/frontend/iteration-8-testing/tasks/task-25-automated-tests/summary.md) |

---

## Итерация 0 — Требования к UI и API-контракты ✅

### Цель

Зафиксировать функциональные требования к 5 экранам и общим компонентам; спроектировать API-контракты для всех экранов frontend; обновить `docs/tech/api-contracts.md`.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-0-ui-contracts/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-0-ui-contracts/summary.md)

---

### Задача 01: Функциональные требования к экранам ✅

#### Цель

Зафиксированы требования к 5 экранам, общей навигации, темам и адаптивности в едином документе.

#### Состав работ

- Описать Экран 1 — Форма входа: поля логин/пароль, выбор роли (Преподаватель / Ученик), простая авторизация без верификации по e-mail
- Описать Экран 2 — Календарь Преподавателя: недельная сетка расписания, лента bot-запросов (10 шт.), запросы на перенос, блоки неподтверждённых занятий и несданных ДЗ; CRUD занятий
- Описать Экран 3 — Ученики (Преподаватель): 2 представления (карточки / таблица), CRUD учеников; детальная форма с историей занятий, счётчиками, лентой диалога с ботом
- Описать Экран 4 — Настройки системы (Преподаватель): имя репетитора, длительность по умолчанию, интервалы напоминаний
- Описать Экран 5 — Расписание Ученика: календарь занятий с деталями
- Описать общие компоненты: боковая навигация с ролевой фильтрацией, header с переключателем темы, кнопка выхода, мобильный drawer
- Зафиксировать стиль: 2 цветовые схемы (light/dark), выбор пользователем, адаптивность всех форм
- Зафиксировать выбор дизайн-системы и компонентной библиотеки

#### Артефакты

- **`docs/spec/frontend-requirements.md`** — основной документ с требованиями (создаётся в этой задаче); структура:
  - Раздел per экран: цель, доступные роли, список компонентов, действия пользователя, edge cases
  - Раздел «Общие компоненты»: навигация, header, drawer, ThemeToggle
  - Раздел «Аутентификация»: механизм, роли, редиректы
  - Раздел «Дизайн-система»: выбранный стек (shadcn/ui + Tailwind), темы light/dark, адаптивность
- `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/plan.md`
- `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/summary.md`

#### Definition of Done

**Агент:**

- [x] `docs/spec/frontend-requirements.md` создан и содержит все 5 экранов: цель, роли, компоненты, действия
- [x] Зафиксированы общие компоненты и навигационная структура
- [x] Указан принцип аутентификации: без email-верификации, JWT httpOnly cookie
- [x] Требования согласованы с `docs/vision.md` (тонкий клиент, роли student/teacher)

**Пользователь:**

- [x] Открыть `docs/spec/frontend-requirements.md` — прочитать описание всех экранов
- [x] Убедиться, что роли, экраны и доступные действия соответствуют ожиданиям

#### Документы

- 📋 [План](impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/plan.md)
- 📝 [Summary](impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/summary.md)

---

### Задача 02: API-контракты для frontend ✅

#### Цель

Спроектированы контракты всех новых endpoints, необходимых для отрисовки 5 экранов; `docs/tech/api-contracts.md` обновлён.

#### Состав работ

- Спроектировать auth-контракты: `POST /v1/auth/login`, `POST /v1/auth/logout`, `GET /v1/auth/me`
- Спроектировать контракты для Экрана 2 (Календарь):
  - `GET /v1/teacher/schedule?week_start=YYYY-MM-DD` — недельное расписание
  - `GET /v1/teacher/bot-requests?limit=10` — лента bot-запросов
  - `GET /v1/teacher/unconfirmed-lessons?days=2` — неподтверждённые занятия
  - `GET /v1/teacher/pending-homework?days=2` — несданные ДЗ
  - `POST /v1/teacher/remind-unconfirmed` — напомнить всем неподтвердившим
  - `POST /v1/teacher/remind-pending-homework` — напомнить всем несдавшим ДЗ
  - `GET /v1/teacher/reschedule-requests` — запросы на перенос
  - `PATCH /v1/teacher/reschedule-requests/{id}` — принять/отклонить запрос
- Спроектировать контракты для Экрана 3 (Ученики):
  - `GET /v1/students` — список учеников
  - `POST /v1/students` — создать ученика
  - `GET /v1/students/{id}` — детали ученика
  - `PUT /v1/students/{id}` — обновить ученика
  - `DELETE /v1/students/{id}` — удалить ученика
  - `GET /v1/students/{id}/lessons` — история занятий ученика
  - `GET /v1/students/{id}/dialogue` — лента диалога ученика с ботом
- Спроектировать контракты для Экрана 4 (Настройки): `GET /v1/settings`, `PUT /v1/settings`
- Спроектировать контракты для Экрана 5 (Расписание ученика): `GET /v1/students/{id}/schedule?month=YYYY-MM`
- Расширить контракты CRUD занятий: `POST /v1/lessons`, `GET /v1/lessons/{id}`, `PUT /v1/lessons/{id}`, `DELETE /v1/lessons/{id}`, `PATCH /v1/lessons/{id}/flags`
- Проверить контракты по skill `api-design-principles`
- Обновить `docs/tech/api-contracts.md`: добавить новый раздел «API для frontend»

#### Артефакты

- `docs/tech/api-contracts.md` — обновлён, раздел «API для frontend»
- `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/plan.md`
- `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/summary.md`

#### Definition of Done

**Агент:**

- [x] Все новые маршруты описаны: метод, путь, request/response-схема, HTTP-коды
- [x] Покрыты все 5 экранов и CRUD занятий с флагами
- [x] Проверено по skill `api-design-principles` — нет нарушений именования, консистентности
- [x] `docs/tech/api-contracts.md` обновлён и не содержит дублирования с уже существующими контрактами

**Пользователь:**

- [x] Открыть `docs/tech/api-contracts.md` — проверить наличие раздела «API для frontend»
- [x] Убедиться, что все экраны покрыты endpoints

#### Документы

- 📋 [План](impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/plan.md)
- 📝 [Summary](impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/summary.md)

---

## Итерация 1 — Реализация API для frontend ✅

### Цель

Реализовать в backend все endpoints, спроектированные в Итерации 0; расширить схему данных; наполнить БД mock-данными; добавить преподавателя в БД.

### Навыки для итерации

При реализации задач 03–06 применять:

- **`api-design-principles`** — URL как ресурсы во мн.ч. (`/students`, `/lessons`), HTTP-методы по семантике, единый `ErrorResponse`, статус-коды (201 при создании, 204 при удалении, 404/409 по ситуации), `PaginatedResponse` для list-эндпоинтов; при отклонении от уже зафиксированных контрактов `docs/tech/api-contracts.md` — обновить файл.
- **`fastapi-templates`** — каждый домен в своём файле роутера (`auth.py`, `teacher.py`, `students.py`, `settings.py`); `Depends(get_db)` для сессии; `Depends(get_current_user)` для JWT-защиты; `response_model=` на каждом эндпоинте; сервисный слой — `services/`, ORM-модели — `storage/models.py`, репозитории — `storage/repositories/`.
- **`modern-python`** — новые зависимости добавлять через `uv add` (не вручную); dev/test-зависимости — в `[dependency-groups]`; `uv run pytest` в Makefile-цели `backend-test`; зависимости для bcrypt/JWT — в основную группу, не в dev.
- **`postgresql-table-design`** — применять при любом изменении схемы (задача 03): типы данных, индексы на FK-колонках, `NOT NULL` + `DEFAULT`, `TIMESTAMPTZ`, `TEXT`, `BIGINT GENERATED ALWAYS AS IDENTITY`.
- **`sharp-edges`** — применять при реализации auth (задача 04): JWT-алгоритм не из заголовка токена, `SECRET_KEY` обязателен при старте, срок жизни токена валидируется на корректность, `password_hash` хранится только через bcrypt без выбора алгоритма пользователем.

> Обновлять артефакты в той же задаче: `docs/data-model.md` при изменении схемы, `docs/tech/api-contracts.md` при отклонениях от проекта, `.env.example` при новых переменных окружения.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-1-backend-api/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-1-backend-api/summary.md)

---

### Задача 03: Анализ пробелов схемы данных 📋

#### Цель

Выявлены и задокументированы все расхождения между текущей схемой `docs/data-model.md` и требованиями 5 экранов; сформулированы изменения для реализации.

#### Состав работ

- Сравнить требования Итерации 0 с текущей схемой `docs/data-model.md`
- Выявить отсутствующие поля и таблицы; при проектировании типов соблюдать правила `postgresql-table-design`:
  - `lessons`: 5 bool-флагов — `BOOLEAN NOT NULL DEFAULT false` (не nullable bool, не int): `notification_sent`, `confirmed_by_student`, `homework_sent`, `solution_received`, `solution_checked`
  - Новая таблица `reschedule_requests`: PK — `BIGINT GENERATED ALWAYS AS IDENTITY`; `lesson_id BIGINT NOT NULL REFERENCES lessons(id)`, `student_id BIGINT NOT NULL REFERENCES users(id)`; `requested_at TIMESTAMPTZ NOT NULL DEFAULT now()`; `proposed_time TIMESTAMPTZ NOT NULL`; `status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected'))`; обязательно добавить `CREATE INDEX ON reschedule_requests (lesson_id)` и `CREATE INDEX ON reschedule_requests (student_id)` — FK не индексируются автоматически
  - Новая таблица `system_settings`: `key TEXT PRIMARY KEY` (не `VARCHAR(n)`), `value TEXT NOT NULL`
  - Расширение `users`: `password_hash TEXT` (не `VARCHAR`); `NOT NULL` добавить только если все существующие записи будут иметь хеш (иначе nullable с `DEFAULT NULL` до миграции данных)
- Описать необходимые миграции Alembic; имена миграций — по шаблону `YYYY_MM_DD_NNN_<slug>.py`; добавление `NOT NULL`-колонки с волатильным DEFAULT вызывает полный rewrite таблицы — использовать двухшаговую миграцию (add nullable → backfill → set NOT NULL) если таблица уже содержит данные
- Обновить `docs/data-model.md`: добавить новые таблицы, поля, FK, индексы

#### Артефакты

- `docs/data-model.md` — обновлён: новые таблицы, поля, FK, индексы
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/plan.md`
- `docs/tasks/impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/summary.md`

#### Definition of Done

**Агент:**

- [ ] Все пробелы перечислены в summary с обоснованием
- [ ] `docs/data-model.md` обновлён: новые таблицы, поля, FK, индексы
- [ ] Нет `VARCHAR(n)`, `TIMESTAMP` (без TZ), `SERIAL`, nullable bool-флагов в новых таблицах
- [ ] FK-колонки в `reschedule_requests` имеют явные индексы
- [ ] Нет противоречий с уже принятыми ADR
- [ ] Применены правила: `postgresql-table-design` (типы, NOT NULL, FK-индексы, CHECK для статусов)

**Пользователь:**

- [ ] Открыть `docs/data-model.md` — убедиться в наличии `reschedule_requests`, `system_settings` и флагов в `lessons`

#### Документы

- 📋 [План](impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/plan.md)
- 📝 [Summary](impl/frontend/iteration-1-backend-api/tasks/task-03-data-gaps/summary.md)

---

### Задача 04: Новые endpoints backend 📋

#### Цель

Реализованы все endpoints из Итерации 0 в `backend/src/ttlg_backend/`; написаны миграции Alembic для новых таблиц и полей; smoke-тесты проходят.

#### Состав работ

- Создать миграции Alembic для изменений из Задачи 03; применить `alembic upgrade head`
- Реализовать **auth-роутер** `api/auth.py`: `POST /v1/auth/login` (bcrypt + JWT, возвращает `200` с токеном, следовать контракту из api-contracts.md), `POST /v1/auth/logout` (`204`), `GET /v1/auth/me` (`200`)
  - JWT-зависимость: `Depends(get_current_user)` — вынести в `api/deps.py`, не дублировать
  - `password_hash` — bcrypt через `passlib`; добавить через `uv add passlib[bcrypt]`
  - **`sharp-edges` — безопасность JWT**: алгоритм подписи задаётся только на сервере (константа `ALGORITHM = "HS256"`), **никогда не читается из заголовка токена**; при декодировании передавать `algorithms=["HS256"]` явно, не `algorithms=[header["alg"]]`
  - **`sharp-edges` — опасные конфиги**: `SECRET_KEY` валидируется при старте через `pydantic-settings` — пустая строка или отсутствие должны поднимать `ValidationError`, не молча приниматься; `ACCESS_TOKEN_EXPIRE_MINUTES` должен быть `> 0`, иначе — ошибка конфигурации (значение `0` не означает «не истекает»)
  - **`sharp-edges` — хеширование**: выбор алгоритма хеширования паролей не конфигурируется снаружи — только `bcrypt`, жёстко в коде сервиса; возврат `True` из `verify_password` при пустом хеше недопустим — всегда проверять длину/наличие хеша
- Реализовать **teacher-роутер** `api/teacher.py`: dashboard-endpoints (schedule, bot-requests, unconfirmed, pending-hw, reminders, reschedule-requests); все list-эндпоинты возвращают `PaginatedResponse` или `list` с явным `response_model=`
- Реализовать **students-роутер** `api/students.py`: CRUD (`GET /v1/students` — list с пагинацией, `POST` — `201`, `GET /{id}` — `200`/`404`, `PUT /{id}` — `200`/`404`, `DELETE /{id}` — `204`/`404`) + `GET /v1/students/{id}/lessons`, `GET /v1/students/{id}/dialogue`
- Реализовать **settings-роутер** `api/settings.py`: `GET /v1/settings` (`200`), `PUT /v1/settings` (`200`)
- Расширить **lessons-роутер** `api/lessons.py`: полный CRUD, `PATCH /v1/lessons/{id}/flags` (`200`/`404`)
- Каждый роутер: бизнес-логика в `services/`, ORM-запросы в `storage/repositories/` (паттерн из `fastapi-templates`)
- Единый формат ошибок: `{"error": "...", "message": "...", "details": {...}}` — реализовать через `HTTPException` или `exception_handler` (правило `api-design-principles`)
- Все новые зависимости устанавливать через `uv add`, не редактировать `pyproject.toml` вручную (`modern-python`)
- Написать smoke-тесты на ключевые endpoints: happy path + 401 без токена; `uv add --group dev pytest-asyncio httpx`
- **Обновить `docs/tech/api-contracts.md`** при любых отклонениях от проекта (изменения полей, кодов, путей)

#### Артефакты

- `backend/src/ttlg_backend/api/auth.py`
- `backend/src/ttlg_backend/api/teacher.py`
- `backend/src/ttlg_backend/api/students.py`
- `backend/src/ttlg_backend/api/settings.py`
- `backend/src/ttlg_backend/api/lessons.py`
- `backend/src/ttlg_backend/api/deps.py` — общие Depends (get_current_user, get_db)
- `backend/src/ttlg_backend/services/` — сервисы по домену
- `backend/src/ttlg_backend/storage/models.py` — расширен
- `backend/alembic/versions/` — новые миграции
- `backend/tests/` — smoke-тесты
- `docs/tech/api-contracts.md` — обновлён при отклонениях

#### Definition of Done

**Агент:**

- [ ] Все endpoint'ы из Итерации 0 реализованы и доступны в OpenAPI `/docs`
- [ ] Каждый роутер имеет `response_model=` — нет «голых» эндпоинтов без схемы
- [ ] Единый формат ошибок — нет `detail: str` в ответах 4xx/5xx (только структурированный `dict`)
- [ ] List-эндпоинты возвращают пагинированный результат (даже если `limit=100`)
- [ ] Миграции применяются без ошибок: `alembic upgrade head`
- [ ] `make backend-test` — все тесты зелёные
- [ ] JWT-защита работает: запросы без токена возвращают `401`
- [ ] `docs/tech/api-contracts.md` соответствует реализации
- [ ] JWT-алгоритм зафиксирован на сервере, не читается из токена; `algorithms=["HS256"]` явно при декодировании
- [ ] `SECRET_KEY=""` при старте поднимает ошибку (не принимается молча)
- [ ] `verify_password` не возвращает `True` при пустом хеше
- [ ] Применены правила: `api-design-principles` (коды, формат ошибок, ресурсы), `fastapi-templates` (Depends, service layer, response_model), `modern-python` (uv add, dependency-groups), `sharp-edges` (JWT, пароли, конфиги)

**Пользователь:**

- [ ] Запустить `make backend-run` → открыть `http://localhost:8000/docs`
- [ ] Убедиться в наличии разделов auth, teacher, students, settings
- [ ] Выполнить `POST /v1/auth/login` с тестовыми данными — получить токен

#### Документы

- 📋 [План](impl/frontend/iteration-1-backend-api/tasks/task-04-new-endpoints/plan.md)
- 📝 [Summary](impl/frontend/iteration-1-backend-api/tasks/task-04-new-endpoints/summary.md)

---

### Задача 05: Миграция с mock-данными 📋

#### Цель

В БД после `alembic upgrade head` присутствуют тестовые данные, достаточные для демонстрации всех экранов frontend.

#### Состав работ

- Создать Alembic-миграцию с seed-данными (отдельный файл миграции — не смешивать с DDL-миграциями):
  - 4–6 учеников с профилями (имя, класс, телефон, email, telegram_id)
  - 20–30 занятий за последние 4 недели и ближайшие 2 недели с разными статусами и флагами
  - 10–15 домашних заданий с разными статусами (`pending`, `submitted`, `overdue`)
  - 2–3 диалога с историей сообщений (8–12 сообщений каждый)
  - 2–3 запроса на перенос занятий
  - Дефолтные настройки системы в `system_settings`
- Проверить, что данные корректно отображаются при запросах к API (через `make backend-run` + Swagger)

#### Артефакты

- `backend/alembic/versions/` — миграция seed-данных

#### Definition of Done

**Агент:**

- [ ] Миграция применяется без ошибок
- [ ] `GET /v1/teacher/schedule` возвращает непустые данные
- [ ] `GET /v1/students` возвращает ≥ 4 учеников
- [ ] `GET /v1/teacher/bot-requests` возвращает ≥ 5 записей

**Пользователь:**

- [ ] Выполнить `make backend-migrate` → убедиться, что миграция прошла
- [ ] Открыть `GET /v1/students` в Swagger — увидеть список учеников

#### Документы

- 📋 [План](impl/frontend/iteration-1-backend-api/tasks/task-05-mock-migration/plan.md)
- 📝 [Summary](impl/frontend/iteration-1-backend-api/tasks/task-05-mock-migration/summary.md)

---

### Задача 06: Миграция преподавателя в БД 📋

#### Цель

Преподаватель Владимир (vzolotoy@mail.ru) добавлен в БД через Alembic-миграцию с хешированным паролем; `.env.example` актуализирован.

#### Состав работ

- Создать Alembic-миграцию: вставить запись `users` с `role=teacher`, `name="Владимир"`, `email="vzolotoy@mail.ru"`, `password_hash` (bcrypt от `TEACHER_DEFAULT_PASSWORD` из env или хардкод дефолта для dev — в prod всегда переменная)
- Хеширование делать в самой миграции через `passlib.hash.bcrypt.hash()` — не хранить пароль в открытом виде в коде
- Добавить в `.env.example` переменную `TEACHER_DEFAULT_PASSWORD` с комментарием; `.env` в git не коммитить (`modern-python`: секреты не в коде)
- Убедиться, что логин работает через `POST /v1/auth/login`

#### Артефакты

- `backend/alembic/versions/` — миграция добавления преподавателя
- `.env.example` — актуализирован

#### Definition of Done

**Агент:**

- [ ] Миграция применяется без ошибок
- [ ] `POST /v1/auth/login` с данными преподавателя возвращает `200` и JWT-токен
- [ ] `.env.example` содержит все новые переменные

**Пользователь:**

- [ ] Выполнить `make backend-migrate`
- [ ] В Swagger выполнить `POST /v1/auth/login` с email `vzolotoy@mail.ru` — получить токен

#### Документы

- 📋 [План](impl/frontend/iteration-1-backend-api/tasks/task-06-teacher-migration/plan.md)
- 📝 [Summary](impl/frontend/iteration-1-backend-api/tasks/task-06-teacher-migration/summary.md)

---

## Итерация 2 — Каркас frontend-проекта ✅

### Цель

Инициализирован и настроен проект `frontend/`; работают темы, форма входа, общий layout с навигацией; настроена маршрутизация по ролям; добавлены Makefile-цели.

### Навыки для итерации

При реализации задач 07–11 применять:

- **`shadcn`** — инициализация через CLI, подбор и добавление компонентов, семантические токены, правила форм (`FieldGroup`/`Field`), правила доступности (`SheetTitle`, `AvatarFallback`), правила стилизации (`gap-*`, `cn()`, `size-*`, `Separator`, `Skeleton`).
- **`vercel-react-best-practices`** — Server/Client split, предотвращение мигания темы (`rendering-hydration-no-flicker`), ленивая загрузка компонентов (`bundle-dynamic-imports`), запрет barrel-файлов (`bundle-barrel-imports`), `React.cache()` для дедупликации (`server-cache-react`), минимизация сериализации в RSC props (`server-serialization`).
- **`nextjs-app-router-patterns`** — файловые конвенции App Router (`loading.tsx`, `error.tsx`, `not-found.tsx`), Server Actions для мутаций, Route Handlers для API, потоковая передача с `Suspense`, `metadata` в layout, кэширование через `fetch` + `next.revalidate`/`tags`.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-2-scaffold/plan.md)
- ✅ [Summary итерации](impl/frontend/iteration-2-scaffold/summary.md)

**Приёмка:** автоматические `frontend-lint` / `frontend-build` и ручной смоук по чек-листу зафиксированы в [summary итерации 2](impl/frontend/iteration-2-scaffold/summary.md) (раздел «Проверки», 2026-04-15).

---

### Задача 07: Инициализация проекта Next.js ✅

#### Цель

Создан `frontend/` с настроенным стеком: Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui; проект запускается.

#### Состав работ

- Инициализировать проект: `pnpm create next-app frontend --typescript --tailwind --app --src-dir`
- Инициализировать shadcn/ui через CLI: `pnpm dlx shadcn@latest init`; выбрать preset с поддержкой Tailwind v4 (если доступен — `base-nova` или `radix-nova`); проверить `components.json` — убедиться в корректных `aliases`, `tailwindVersion`, `tailwindCssFile`
- Получить контекст проекта: `pnpm dlx shadcn@latest info --json` — зафиксировать `isRSC`, `base`, `iconLibrary`, `packageManager` для последующих задач
- Настроить `frontend/tsconfig.json`, `frontend/next.config.ts`, `frontend/.eslintrc.json`
- Создать корневой `frontend/src/app/layout.tsx` с `metadata` export и `suppressHydrationWarning` на `<html>` (паттерн App Router: `metadata` — только в Server Components); `Providers` — отдельный Client Component (`providers.tsx`)
- Создать общий `frontend/src/app/not-found.tsx` — страница 404 (файловая конвенция App Router)
- Добавить базовые shadcn-компоненты командой CLI (не вручную): `pnpm dlx shadcn@latest add button input card dialog sheet badge separator label switch skeleton alert empty`; после добавления **прочитать добавленные файлы** и убедиться в корректном составе компонентов и импортах
- Настроить импорты: **запретить barrel-файлы** (`index.ts` с реэкспортами) — каждый модуль импортировать напрямую (правило `bundle-barrel-imports`)
- Создать `frontend/.env.local.example` с `NEXT_PUBLIC_API_URL`
- Проверить: `pnpm --filter frontend dev` запускает dev-сервер; `pnpm --filter frontend build` проходит без ошибок

#### Артефакты

- `frontend/` — инициализированный проект
- `frontend/src/app/layout.tsx` — корневой layout с `metadata` и `Providers`
- `frontend/src/app/not-found.tsx`
- `frontend/src/components/providers.tsx`
- `frontend/.env.local.example`
- `frontend/components.json` — конфиг shadcn

#### Definition of Done

**Агент:**

- [ ] `pnpm --filter frontend dev` запускается без ошибок
- [ ] `pnpm --filter frontend build` завершается успешно
- [ ] Подключён shadcn/ui: `components.json` присутствует, базовые компоненты установлены через CLI
- [ ] `pnpm dlx shadcn@latest info` возвращает корректные `aliases`, `isRSC=true`, `tailwindCssFile`
- [ ] `layout.tsx` содержит `export const metadata`; `<html suppressHydrationWarning>`
- [ ] `not-found.tsx` создан и доступен по несуществующему URL
- [ ] TypeScript-ошибок нет; barrel-файлов в `src/` нет
- [ ] Применены skills: `shadcn` (инициализация, проверка конфига), `nextjs-app-router-patterns` (файловые конвенции, metadata)

**Пользователь:**

- [ ] Выполнить `make frontend-dev` → открыть `http://localhost:3000` — видна стартовая страница
- [ ] Открыть `frontend/components.json` — убедиться в конфиге shadcn

#### Документы

- 📋 [План](impl/frontend/iteration-2-scaffold/tasks/task-07-project-init/plan.md)
- 📝 [Summary](impl/frontend/iteration-2-scaffold/tasks/task-07-project-init/summary.md)

---

### Задача 08: Темы — светлая и тёмная ✅

#### Цель

Настроены CSS-переменные shadcn для light/dark схем; подключён `next-themes`; пользователь может переключать тему без мигания при загрузке.

#### Состав работ

- Установить `next-themes`: `pnpm --filter frontend add next-themes`
- Обернуть `layout.tsx` в `ThemeProvider` (attribute="class", `defaultTheme="system"`, `enableSystem`); `ThemeProvider` — Client Component-обёртка, вынести в отдельный файл `providers.tsx`
- Настроить CSS-переменные **только в `tailwindCssFile`** (файл из `components.json`, обычно `globals.css`) — **не создавать отдельные CSS-файлы**; использовать **исключительно семантические токены** shadcn (`--background`, `--foreground`, `--primary` и т.д.) — никаких `bg-blue-500` или `bg-gray-900`
- Запретить ручные `dark:`-переопределения цветов в компонентах — тема управляется CSS-переменными (правило `shadcn`: «No manual `dark:` color overrides»)
- Создать `ThemeToggle` — Client Component (`"use client"`); иконки из `iconLibrary` проекта (`data-icon`); обернуть в `Button variant="ghost"`
- **Предотвратить мигание при загрузке** (правило `rendering-hydration-no-flicker`): добавить `suppressHydrationWarning` на `<html>`; `next-themes` с `attribute="class"` уже решает проблему, но явно задокументировать в summary

#### Артефакты

- `frontend/src/app/layout.tsx` — ThemeProvider
- `frontend/src/app/globals.css` — CSS-переменные (только семантические токены)
- `frontend/src/components/theme-toggle.tsx`
- `frontend/src/components/providers.tsx` — Client-обёртка провайдеров

#### Definition of Done

**Агент:**

- [ ] Компонент `ThemeToggle` переключает классы `light`/`dark` на `<html>`
- [ ] CSS-переменные shadcn корректно применяются в обеих темах — нет raw-цветов в `globals.css`
- [ ] Выбор темы сохраняется в `localStorage`; страница не мигает при перезагрузке (нет FOUC)
- [ ] `ThemeProvider` изолирован в `providers.tsx`, `layout.tsx` остаётся Server Component
- [ ] Применены правила: `shadcn` (семантические токены, `tailwindCssFile`), `rendering-hydration-no-flicker`

**Пользователь:**

- [ ] Открыть `http://localhost:3000` → нажать `ThemeToggle` — тема переключается
- [ ] Обновить страницу — тема сохранена, мигания нет

#### Документы

- 📋 [План](impl/frontend/iteration-2-scaffold/tasks/task-08-themes/plan.md)
- 📝 [Summary](impl/frontend/iteration-2-scaffold/tasks/task-08-themes/summary.md)

---

### Задача 09: Форма входа и защищённые роуты ✅

#### Цель

Реализована страница `/login` с формой (email + пароль); аутентификация через `POST /v1/auth/login`; JWT хранится в `httpOnly` cookie; незаутентифицированный доступ к защищённым роутам редиректит на `/login`.

#### Состав работ

- Создать страницу `frontend/src/app/(auth)/login/page.tsx` — Server Component; форма email + пароль, кнопка «Войти»
  - Форма строится через **`FieldGroup + Field + FieldLabel + Input`** (shadcn) — никаких raw `<div>` с `space-y-*` для формы
  - Ошибки валидации: `data-invalid` на `<Field>`, `aria-invalid` на `<Input>` (shadcn: «Field validation uses `data-invalid` + `aria-invalid`»)
  - Кнопка в состоянии pending: `Button disabled` + `Spinner` (не `isPending`-проп, которого у `Button` нет)
  - `Alert` для серверных ошибок («Неверный логин или пароль») — не кастомный `div`
- **Server Action** `frontend/src/app/actions/auth.ts` — `"use server"`: принимает `formData`, вызывает `POST /v1/auth/login`, устанавливает `httpOnly` cookie через `cookies()` из `next/headers`, после успеха вызывает `redirect()` из `next/navigation` по роли (паттерн App Router: Server Actions для мутаций с progressive enhancement); валидировать входные данные до обращения к API (правило `server-auth-actions`)
- **Route Handler** `frontend/src/app/api/auth/logout/route.ts` — очистка cookie через `NextResponse`; этот endpoint вызывается из Client Component кнопки «Выйти»
- Запускать fetch к backend API **без последовательного ожидания**: токен декодировать сразу после получения, роль определять синхронно — не создавать лишних последовательных await (правило `async-defer-await`)
- Создать `frontend/src/middleware.ts`: проверка cookie, редирект на `/login` если нет токена; редирект на нужный роут по роли из JWT; middleware — **тонкий**: только cookie-проверка, без тяжёлой логики
- Создать `frontend/src/lib/auth.ts`: утилиты `getSession()`, `getUser()`; использовать `React.cache()` для дедупликации повторных вызовов в одном render-запросе (правило `server-cache-react`)

#### Артефакты

- `frontend/src/app/(auth)/login/page.tsx`
- `frontend/src/app/actions/auth.ts` — Server Action (`"use server"`)
- `frontend/src/app/api/auth/logout/route.ts`
- `frontend/src/middleware.ts`
- `frontend/src/lib/auth.ts`

#### Definition of Done

**Агент:**

- [ ] Форма входа: `FieldGroup + Field + Input` — нет raw `<div className="space-y-*">`
- [ ] Ошибки валидации через `data-invalid` / `aria-invalid` (shadcn-паттерн)
- [ ] Логин реализован через Server Action (`"use server"`); `cookies()` из `next/headers`; `redirect()` после успеха
- [ ] JWT сохраняется в `httpOnly` cookie (не виден в JS)
- [ ] `/teacher/*` без токена → редирект на `/login`
- [ ] После входа преподаватель попадает на `/teacher/calendar`
- [ ] Кнопка выхода очищает cookie (Route Handler) и редиректит на `/login`
- [ ] `getUser()` обёрнут в `React.cache()` — без дублирования вызовов
- [ ] Применены правила: `shadcn` (FieldGroup, Alert, Button+Spinner), `nextjs-app-router-patterns` (Server Action, Route Handler, cookies, redirect), `server-auth-actions`, `server-cache-react`, `async-defer-await`

**Пользователь:**

- [ ] Открыть `http://localhost:3000/login` — видна форма входа
- [ ] Войти с данными преподавателя → попасть на `/teacher/calendar`
- [ ] Открыть DevTools → Application → Cookies: JWT в `httpOnly` cookie
- [ ] Выйти → попасть на `/login`

#### Документы

- 📋 [План](impl/frontend/iteration-2-scaffold/tasks/task-09-auth/plan.md)
- 📝 [Summary](impl/frontend/iteration-2-scaffold/tasks/task-09-auth/summary.md)

---

### Задача 10: Общий layout — навигация, header, drawer ✅

#### Цель

Реализован общий layout для аутентифицированных пользователей: боковая навигация (desktop), мобильный drawer (sheet), верхняя панель с ThemeToggle и кнопкой выхода.

#### Состав работ

- Создать `frontend/src/app/(app)/layout.tsx` — **Server Component**; получает пользователя через `getUser()` (серверная утилита); передаёт только необходимые данные (имя, роль) в Client Components (правило `server-serialization` — не сериализовывать лишнее); добавить `export const metadata` для этой группы роутов
- Создать `frontend/src/app/(app)/error.tsx` — **Client Component** (`"use client"`); Error Boundary для аутентифицированной зоны (файловая конвенция App Router: `error.tsx` автоматически оборачивает `page.tsx` в Suspense-like error boundary)
- Перед реализацией sidebar/navigation: `pnpm dlx shadcn@latest search @shadcn -q "sidebar"` и `pnpm dlx shadcn@latest search @shadcn -q "navigation"` — проверить наличие готового компонента (правило shadcn: «Use existing components first»)
- Создать `frontend/src/components/sidebar.tsx`: ссылки навигации с иконками из `iconLibrary`, фильтрация по роли (teacher / student); активный пункт — через `usePathname()` + `cn()` (не ручной ternary в `className`)
  - Преподаватель: Календарь, Ученики, Настройки
  - Ученик: Расписание
  - Разделители между группами — `<Separator>` (не `<hr>` или `<div className="border-t">`)
- Создать `frontend/src/components/header.tsx`: название страницы, `ThemeToggle`, аватар (`Avatar + AvatarFallback` — всегда с fallback), кнопка «Выйти»
- Создать `frontend/src/components/mobile-nav.tsx`: `Sheet` из shadcn — **обязательно** содержит `SheetTitle` (для accessibility; `className="sr-only"` если визуально скрыт)
- **Ленивая загрузка мобильного drawer**: `next/dynamic` для `MobileNav` — загружается только при viewport < 768px (правило `bundle-dynamic-imports`); статически импортировать только desktop sidebar
- Адаптивность: sidebar `hidden md:flex`, header показывает hamburger `flex md:hidden`; использовать `gap-*` — не `space-x-*` / `space-y-*` (правило shadcn)
- Статические элементы (логотип, иконки брендинга) — вынести в константы вне компонента (правило `server-hoist-static-io` / `rendering-hoist-jsx`)

#### Артефакты

- `frontend/src/app/(app)/layout.tsx`
- `frontend/src/app/(app)/error.tsx`
- `frontend/src/components/sidebar.tsx`
- `frontend/src/components/header.tsx`
- `frontend/src/components/mobile-nav.tsx`

#### Definition of Done

**Агент:**

- [ ] `layout.tsx` — Server Component; Client Components получают только минимально необходимые props
- [ ] `error.tsx` создан как `"use client"` Error Boundary
- [ ] Layout обёртывает все аутентифицированные страницы
- [ ] Боковая навигация отображается на desktop (≥ 768px), скрыта на mobile
- [ ] На mobile — hamburger открывает `Sheet` с `SheetTitle` (доступность)
- [ ] Активный пункт меню через `usePathname()` + `cn()` — нет ручных ternary в строке className
- [ ] `Avatar` содержит `AvatarFallback`; иконки из `iconLibrary` проекта
- [ ] `MobileNav` загружается через `next/dynamic` (lazy)
- [ ] Нет `space-x-*` / `space-y-*`; нет raw `<hr>` — только `<Separator>`
- [ ] ThemeToggle и кнопка выхода в header работают
- [ ] Применены правила: `shadcn` (Sheet+SheetTitle, Avatar+Fallback, Separator, cn(), gap-*), `nextjs-app-router-patterns` (layout, error.tsx), `server-serialization`, `bundle-dynamic-imports`, `rendering-hoist-jsx`

**Пользователь:**

- [ ] Открыть `http://localhost:3000/teacher/calendar` на desktop — видна sidebar
- [ ] Открыть на mobile (или DevTools 375px) — видна hamburger-кнопка, drawer открывается
- [ ] Нажать «Выйти» в header → редирект на `/login`

#### Документы

- 📋 [План](impl/frontend/iteration-2-scaffold/tasks/task-10-layout/plan.md)
- 📝 [Summary](impl/frontend/iteration-2-scaffold/tasks/task-10-layout/summary.md)

---

### Задача 11: Маршрутизация по ролям и Makefile-цели ✅

#### Цель

Настроена маршрутизация: `teacher/*` → экраны преподавателя, `student/*` → экраны ученика; страницы-заглушки используют правильный Server/Client split; добавлены Makefile-цели для frontend.

#### Состав работ

- Создать структуру роутов App Router — страницы-**Server Components** по умолчанию; `"use client"` добавлять только если страница требует `useState`, `useEffect`, обработчики событий или браузерные API (правило shadcn: «`isRSC=true` → нужен `"use client"`»):
  - `frontend/src/app/(app)/teacher/calendar/page.tsx` — заглушка
  - `frontend/src/app/(app)/teacher/students/page.tsx` — заглушка
  - `frontend/src/app/(app)/teacher/settings/page.tsx` — заглушка
  - `frontend/src/app/(app)/student/schedule/page.tsx` — заглушка
- Для каждого роута создать **`loading.tsx`** — файловая конвенция App Router, автоматически оборачивает `page.tsx` в `<Suspense>`; содержимое — `Skeleton` из shadcn, соответствующий будущей разметке экрана (не `animate-pulse div`); создать:
  - `frontend/src/app/(app)/teacher/calendar/loading.tsx`
  - `frontend/src/app/(app)/teacher/students/loading.tsx`
  - `frontend/src/app/(app)/teacher/settings/loading.tsx`
  - `frontend/src/app/(app)/student/schedule/loading.tsx`
- Настроить middleware: редирект по роли (`teacher` → `/teacher/calendar`, `student` → `/student/schedule`); перекрёстный доступ блокировать (teacher на `/student/*` → редирект); логика middleware **не дублирует** логику из Задачи 09 — вынести общую проверку cookie в `frontend/src/lib/auth.ts`
- **Не определять компоненты внутри других компонентов** (правило `rerender-no-inline-components`) — каждая заглушка в отдельном файле
- Добавить в корневой `Makefile`:
  - `frontend-dev`: `pnpm --filter frontend dev`
  - `frontend-build`: `pnpm --filter frontend build`
  - `frontend-lint`: `pnpm --filter frontend lint`
  - `frontend-test`: `pnpm --filter frontend test` (placeholder)
- Обновить цель `check` в `Makefile`: включить `frontend-lint`

#### Артефакты

- `frontend/src/app/(app)/teacher/` — структура роутов (заглушки + `loading.tsx`)
- `frontend/src/app/(app)/student/` — структура роутов (заглушки + `loading.tsx`)
- `Makefile` — обновлён

#### Definition of Done

**Агент:**

- [ ] После логина teacher попадает на `/teacher/calendar`, student — на `/student/schedule`
- [ ] Прямой переход teacher на `/student/*` → редирект на `/teacher/calendar`
- [ ] Страницы-заглушки — Server Components; `"use client"` отсутствует без необходимости
- [ ] Каждый роут содержит `loading.tsx` с `Skeleton` — нет `animate-pulse div`
- [ ] Логика проверки cookie не дублируется — переиспользует `lib/auth.ts`
- [ ] `make frontend-dev` запускает dev-сервер
- [ ] `make frontend-lint` проходит без ошибок
- [ ] `make check` включает `frontend-lint`
- [ ] Применены правила: `shadcn` (Skeleton, "use client" только по необходимости), `nextjs-app-router-patterns` (loading.tsx как Suspense-конвенция), `rerender-no-inline-components`

**Пользователь:**

- [ ] Войти как teacher → URL `/teacher/calendar`
- [ ] Запустить `make frontend-lint` — нет ошибок
- [ ] Проверить `Makefile` — наличие `frontend-*` целей

#### Документы

- 📋 [План](impl/frontend/iteration-2-scaffold/tasks/task-11-routing-makefile/plan.md)
- 📝 [Summary](impl/frontend/iteration-2-scaffold/tasks/task-11-routing-makefile/summary.md)

---

## Итерация 3 — Экран Преподавателя: Календарь ✅

### Цель

Реализован полноценный экран Календарь Преподавателя: недельная сетка занятий с CRUD, лента bot-запросов, блоки неподтверждённых занятий, несданных ДЗ и запросов на перенос.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-3-teacher-calendar/plan.md)
- ✅ [Summary итерации](impl/frontend/iteration-3-teacher-calendar/summary.md)

**Приёмка:** ручные проверки по сценариям итерации зафиксированы в [summary итерации 3](impl/frontend/iteration-3-teacher-calendar/summary.md) (раздел «Проверки», 2026-04-16).

---

### Задача 12: Недельная сетка расписания ✅

#### Цель

Реализована недельная сетка: 7 колонок по дням, навигация по неделям, карточки занятий с 5 флагами статуса.

#### Состав работ

- Создать компонент `WeeklySchedule`: 7 колонок (пн–вс), заголовки с датами, навигация «< Предыдущая неделя / Следующая неделя >»
- Создать компонент `LessonCard`: имя ученика, время, тема, 5 цветных флагов-иконок (notification, confirmed, hw_sent, solution_received, solution_checked)
- Загружать данные через `GET /v1/teacher/schedule?week_start=...` (Server Component или SWR/React Query)
- Пустые дни — плейсхолдер «+ Добавить занятие»
- Адаптивность: на mobile — вертикальный список дней, горизонтальный скролл

#### Артефакты

- `frontend/src/components/weekly-schedule.tsx`
- `frontend/src/components/lesson-card.tsx`
- `frontend/src/app/(app)/teacher/calendar/page.tsx` — обновлён

#### Definition of Done

**Агент:**

- [x] Сетка отображает 7 дней с датами
- [x] Занятия из API отображаются в правильных колонках
- [x] 5 флагов визуально различимы (цвет/иконка)
- [x] Навигация по неделям работает, данные перезагружаются

**Пользователь:**

- [x] Открыть `/teacher/calendar` — видна сетка с занятиями из mock-данных
- [x] Нажать «Следующая неделя» — данные обновились

#### Документы

- 📋 [План](impl/frontend/iteration-3-teacher-calendar/tasks/task-12-weekly-schedule/plan.md)
- 📝 [Summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-12-weekly-schedule/summary.md)

---

### Задача 13: Диалог занятия — CRUD, флаги, действия ✅

#### Цель

Реализован диалог создания/редактирования занятия и удаления; все поля и флаги работают.

#### Состав работ

- Создать компонент `LessonDialog` (shadcn `Dialog`): поля — выбор ученика (`Select`), дата/время (`DateTimePicker`), тема (`Input`), комментарий (`Textarea`)
- Добавить секцию флагов: 5 `Switch`-переключателей с подписями
- Добавить кнопки действий: «Отправить ДЗ» (POST к API ДЗ), «Напомнить» (POST `/v1/teacher/remind`), «Прикрепить файл» (placeholder)
- Подключить к кнопке «+ Добавить» и к карточке занятия (редактирование)
- Диалог удаления с подтверждением (`AlertDialog`)
- Обновление данных после CRUD без перезагрузки страницы (optimistic update или refetch)

#### Артефакты

- `frontend/src/components/lesson-dialog.tsx`
- `frontend/src/components/lesson-delete-dialog.tsx`

#### Definition of Done

**Агент:**

- [x] Создание занятия через диалог → занятие появляется в сетке
- [x] Редактирование занятия → изменения сохраняются
- [x] Удаление с подтверждением → занятие исчезает из сетки
- [x] Флаги переключаются через `PATCH /v1/lessons/{id}/flags`
- [x] TypeScript-ошибок нет

**Пользователь:**

- [x] Нажать «+ Добавить занятие» → заполнить форму → сохранить → занятие появилось
- [x] Нажать на карточку занятия → открылся диалог с заполненными полями
- [x] Переключить флаг «Подтверждено учеником» → изменение сохраняется

#### Документы

- 📋 [План](impl/frontend/iteration-3-teacher-calendar/tasks/task-13-lesson-dialog/plan.md)
- 📝 [Summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-13-lesson-dialog/summary.md)

---

### Задача 14: Лента bot-запросов ✅

#### Цель

Реализован блок «Последние запросы учеников» — лента из 10 последних сообщений учеников боту.

#### Состав работ

- Создать компонент `BotRequestsFeed`: список из 10 записей с именем ученика, текстом запроса и временем
- Загружать через `GET /v1/teacher/bot-requests?limit=10`
- Оформить как прокручиваемый список с фиксированной высотой
- Разместить в sidebar-секции экрана Календарь или в отдельной панели

#### Артефакты

- `frontend/src/components/bot-requests-feed.tsx`

#### Definition of Done

**Агент:**

- [x] Список отображает 10 (или меньше, если данных меньше) последних запросов
- [x] Каждая запись содержит имя ученика, текст, время
- [x] При пустом ответе — плейсхолдер «Нет запросов»

**Пользователь:**

- [x] Открыть `/teacher/calendar` — виден блок с bot-запросами из mock-данных

#### Документы

- 📋 [План](impl/frontend/iteration-3-teacher-calendar/tasks/task-14-bot-feed/plan.md)
- 📝 [Summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-14-bot-feed/summary.md)

---

### Задача 15: Блок неподтверждённых занятий ✅

#### Цель

Реализован блок «Неподтверждённые занятия» с фильтром по ближайшим 2 дням и кнопкой «Напомнить всем».

#### Состав работ

- Создать компонент `UnconfirmedLessons`: список занятий (имя ученика, дата/время) из ближайших 2 дней без флага `confirmed_by_student`
- Загружать через `GET /v1/teacher/unconfirmed-lessons?days=2`
- Добавить кнопку «Напомнить всем» → `POST /v1/teacher/remind-unconfirmed` → toast с результатом
- При пустом списке — плейсхолдер «Все ученики подтвердили»

#### Артефакты

- `frontend/src/components/unconfirmed-lessons.tsx`

#### Definition of Done

**Агент:**

- [x] Список фильтруется по 2 дням и флагу подтверждения
- [x] Кнопка «Напомнить всем» отправляет запрос и показывает toast
- [x] При пустом списке — плейсхолдер

**Пользователь:**

- [x] Открыть `/teacher/calendar` — виден блок с неподтверждёнными занятиями (из mock-данных)
- [x] Нажать «Напомнить всем» — появился toast-уведомление

#### Документы

- 📋 [План](impl/frontend/iteration-3-teacher-calendar/tasks/task-15-unconfirmed-lessons/plan.md)
- 📝 [Summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-15-unconfirmed-lessons/summary.md)

---

### Задача 16: Блок несданных ДЗ ✅

#### Цель

Реализован блок «Несданные ДЗ» с фильтром по ближайшим 2 дням и кнопкой «Напомнить всем».

#### Состав работ

- Создать компонент `PendingHomework`: список занятий (имя ученика, тема, дата) без флага `solution_received`
- Загружать через `GET /v1/teacher/pending-homework?days=2`
- Добавить кнопку «Напомнить всем» → `POST /v1/teacher/remind-pending-homework` → toast
- При пустом списке — плейсхолдер «Все ДЗ сданы»

#### Артефакты

- `frontend/src/components/pending-homework.tsx`

#### Definition of Done

**Агент:**

- [x] Список отображает ученика, тему, дату занятия
- [x] Кнопка «Напомнить всем» работает и показывает toast
- [x] При пустом списке — плейсхолдер

**Пользователь:**

- [x] Открыть `/teacher/calendar` — виден блок несданных ДЗ из mock-данных

#### Документы

- 📋 [План](impl/frontend/iteration-3-teacher-calendar/tasks/task-16-pending-hw/plan.md)
- 📝 [Summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-16-pending-hw/summary.md)

---

### Задача 17: Блок запросов на перенос занятий ✅

#### Цель

Реализован блок «Запросы на перенос» со списком запросов учеников и кнопками принять/отклонить.

#### Состав работ

- Создать компонент `RescheduleRequests`: список запросов (имя ученика, текущая дата занятия, предложенное время)
- Загружать через `GET /v1/teacher/reschedule-requests`
- Кнопки «Принять» / «Отклонить» → `PATCH /v1/teacher/reschedule-requests/{id}` с `status: accepted/rejected`
- После действия запись исчезает из списка (optimistic remove)
- При пустом списке — плейсхолдер «Нет запросов на перенос»

#### Артефакты

- `frontend/src/components/reschedule-requests.tsx`

#### Definition of Done

**Агент:**

- [x] Список отображает запросы из mock-данных
- [x] Принять/Отклонить отправляет PATCH-запрос
- [x] После действия запись удаляется из UI без перезагрузки

**Пользователь:**

- [x] Открыть `/teacher/calendar` — виден блок с запросами на перенос
- [x] Нажать «Принять» — запрос исчез из списка

#### Документы

- 📋 [План](impl/frontend/iteration-3-teacher-calendar/tasks/task-17-reschedule-requests/plan.md)
- 📝 [Summary](impl/frontend/iteration-3-teacher-calendar/tasks/task-17-reschedule-requests/summary.md)

---

## Итерация 4 — Экран Ученики 📋

### Цель

Реализован экран «Ученики»: список с переключением карточки/таблица, CRUD; детальная форма ученика с историей занятий, счётчиками и лентой диалога.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-4-students/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-4-students/summary.md)

---

### Задача 18: Список учеников — карточки/таблица, CRUD 📋

#### Цель

Реализована страница `/teacher/students` с двумя представлениями и полным CRUD учеников.

#### Состав работ

- Создать страницу `frontend/src/app/(app)/teacher/students/page.tsx`
- Добавить переключатель `SegmentedControl` (Grid / List): `LayoutGrid` / `Table` иконки
- Представление «Карточки»: компонент `StudentCard` — аватар/инициалы, имя, класс, телефон, email, кнопки «Редактировать» / «Удалить»
- Представление «Таблица»: shadcn `Table` с колонками имя, класс, телефон, email, telegram, действия
- Диалог создания/редактирования ученика: поля name, class_label, phone, email, telegram_id
- Диалог удаления с подтверждением
- Загружать через `GET /v1/students`; CRUD через соответствующие endpoints

#### Артефакты

- `frontend/src/app/(app)/teacher/students/page.tsx`
- `frontend/src/components/student-card.tsx`
- `frontend/src/components/student-table.tsx`
- `frontend/src/components/student-dialog.tsx`

#### Definition of Done

**Агент:**

- [ ] Оба представления отображают данные из API
- [ ] Переключатель сохраняет выбор (localStorage или URL-параметр)
- [ ] CRUD работает: создать / редактировать / удалить ученика
- [ ] Список обновляется без перезагрузки страницы

**Пользователь:**

- [ ] Открыть `/teacher/students` — виден список учеников из mock-данных
- [ ] Переключить вид — данные те же, но другое представление
- [ ] Добавить ученика через диалог → он появился в списке

#### Документы

- 📋 [План](impl/frontend/iteration-4-students/tasks/task-18-students-list/plan.md)
- 📝 [Summary](impl/frontend/iteration-4-students/tasks/task-18-students-list/summary.md)

---

### Задача 19: Детальная форма ученика — занятия и счётчики 📋

#### Цель

Реализована страница `/teacher/students/{id}` с историей занятий со статусами, счётчиками и процентом выполненных ДЗ.

#### Состав работ

- Создать страницу `frontend/src/app/(app)/teacher/students/[id]/page.tsx`
- Секция «Профиль»: имя, класс, контакты
- Секция «Статистика»: всего занятий, завершено, ДЗ выдано / выполнено, процент выполнения (прогресс-бар)
- Секция «История занятий»: таблица или список занятий с датой, темой, статусом и 5 флагами
- Загружать через `GET /v1/students/{id}` и `GET /v1/students/{id}/lessons`

#### Артефакты

- `frontend/src/app/(app)/teacher/students/[id]/page.tsx`
- `frontend/src/components/student-stats.tsx`
- `frontend/src/components/student-lessons-history.tsx`

#### Definition of Done

**Агент:**

- [ ] Страница отображает профиль, счётчики и историю занятий
- [ ] Флаги занятий визуально консистентны с Экраном Календарь
- [ ] Прогресс-бар ДЗ рассчитывается корректно

**Пользователь:**

- [ ] Нажать на ученика в списке → открылась детальная форма
- [ ] Виден список занятий с датами, темами и флагами

#### Документы

- 📋 [План](impl/frontend/iteration-4-students/tasks/task-19-student-detail/plan.md)
- 📝 [Summary](impl/frontend/iteration-4-students/tasks/task-19-student-detail/summary.md)

---

### Задача 20: Лента диалога ученика с ботом 📋

#### Цель

В детальной форме ученика реализована лента диалога ученика с ботом с бесконечным скроллом.

#### Состав работ

- Создать компонент `StudentDialogueFeed`: сообщения пользователя и ассистента, временные метки
- Загружать через `GET /v1/students/{id}/dialogue?limit=20&offset=0`
- Реализовать бесконечный скролл вверх (Intersection Observer) для подгрузки более старых сообщений
- Визуально различать сообщения `role=user` и `role=assistant` (выравнивание, цвет фона)

#### Артефакты

- `frontend/src/components/student-dialogue-feed.tsx`

#### Definition of Done

**Агент:**

- [ ] Лента показывает последние 20 сообщений
- [ ] Скролл вверх подгружает следующую порцию
- [ ] Сообщения user и assistant визуально различимы

**Пользователь:**

- [ ] Открыть детальную форму ученика → видна лента диалога
- [ ] Прокрутить вверх → загрузились более старые сообщения

#### Документы

- 📋 [План](impl/frontend/iteration-4-students/tasks/task-20-student-dialogue/plan.md)
- 📝 [Summary](impl/frontend/iteration-4-students/tasks/task-20-student-dialogue/summary.md)

---

## Итерация 5 — Экран Настройки системы 📋

### Цель

Реализована страница `/teacher/settings` с формой настроек и сохранением через API.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-5-settings/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-5-settings/summary.md)

---

### Задача 21: Форма настроек системы 📋

#### Цель

Реализована страница настроек с 4 полями и кнопками «Сохранить» / «Сбросить».

#### Состав работ

- Создать страницу `frontend/src/app/(app)/teacher/settings/page.tsx`
- Поля формы (react-hook-form + zod-валидация):
  - «Имя репетитора» — `Input`, обязательное
  - «Длительность занятия по умолчанию (мин)» — `Input type=number`, min=30, max=180
  - «Напоминание о занятии за N часов» — `Input type=number`, min=1, max=48
  - «Напоминание о ДЗ за N часов» — `Input type=number`, min=1, max=48
- Загружать текущие значения через `GET /v1/settings`
- «Сохранить» → `PUT /v1/settings` → toast с результатом
- «Сбросить» → восстановить значения из API без сохранения

#### Артефакты

- `frontend/src/app/(app)/teacher/settings/page.tsx`

#### Definition of Done

**Агент:**

- [ ] Форма загружает текущие значения из API
- [ ] Валидация полей через zod: числовые поля в допустимом диапазоне
- [ ] «Сохранить» отправляет `PUT /v1/settings` и показывает toast
- [ ] «Сбросить» восстанавливает значения без запроса к API

**Пользователь:**

- [ ] Открыть `/teacher/settings` — форма заполнена текущими настройками
- [ ] Изменить значение → «Сохранить» → toast «Настройки сохранены»
- [ ] Изменить значение → «Сбросить» → значения вернулись к сохранённым

#### Документы

- 📋 [План](impl/frontend/iteration-5-settings/tasks/task-21-settings-form/plan.md)
- 📝 [Summary](impl/frontend/iteration-5-settings/tasks/task-21-settings-form/summary.md)

---

## Итерация 6 — Расписание Ученика 📋

### Цель

Реализован экран `/student/schedule` — календарь занятий ученика.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-6-student-schedule/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-6-student-schedule/summary.md)

---

### Задача 22: Календарь занятий ученика 📋

#### Цель

Реализована страница `/student/schedule` с месячным и недельным видом расписания ученика.

#### Состав работ

- Создать страницу `frontend/src/app/(app)/student/schedule/page.tsx`
- Переключатель «Месяц / Неделя»
- Месячный вид: сетка месяца, дни с занятиями подсвечены, счётчик занятий на день
- Недельный вид: 7 колонок, карточки занятий (тема, время, статус)
- Клик по занятию → попап/drawer с деталями: тема, ДЗ, статус, заметки
- Загружать через `GET /v1/students/{id}/schedule?month=YYYY-MM`
- Навигация: «< Предыдущий / Следующий месяц (или неделя) >»

#### Артефакты

- `frontend/src/app/(app)/student/schedule/page.tsx`
- `frontend/src/components/student-monthly-calendar.tsx`
- `frontend/src/components/student-weekly-view.tsx`
- `frontend/src/components/lesson-detail-popup.tsx`

#### Definition of Done

**Агент:**

- [ ] Оба вида (месяц/неделя) отображают занятия из API
- [ ] Навигация по месяцам/неделям работает
- [ ] Клик по занятию открывает попап с деталями

**Пользователь:**

- [ ] Войти как ученик → открыть `/student/schedule`
- [ ] Переключить вид месяц/неделя — данные те же, вид разный
- [ ] Нажать на занятие → попап с темой и статусом

#### Документы

- 📋 [План](impl/frontend/iteration-6-student-schedule/tasks/task-22-student-calendar/plan.md)
- 📝 [Summary](impl/frontend/iteration-6-student-schedule/tasks/task-22-student-calendar/summary.md)

---

## Итерация 7 — Ревью качества кода frontend 📋

### Цель

Проверен и исправлен код frontend по best practices Next.js App Router и React; критические замечания устранены. **Цветовая палитра из макетов** внедрена в семантические токены shadcn (`--primary`, `--ring`, `--accent` и др. в `globals.css` для `:root` и `.dark`), без raw-классов в компонентах — визуальное соответствие макетам форм до перехода к финальному тестированию (итерация 8).

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-7-quality-review/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-7-quality-review/summary.md)

---

### Задача 23: Ревью кода по best practices 📋

#### Цель

Проверен весь `frontend/src/` по checklists skills `vercel-react-best-practices` и `nextjs-app-router-patterns`; критические ошибки исправлены; изменения задокументированы. **Согласована тема с цветными макетами:** перенос палитры в CSS-переменные shadcn (light/dark), проверка контраста и акцентов на ключевых экранах.

#### Состав работ

- Применить skill `vercel-react-best-practices`: проверить Server Components vs Client Components, мемоизацию, fetch/caching
- Применить skill `nextjs-app-router-patterns` (если доступен): проверить layout, loading.tsx, error.tsx, metadata
- Проверить bundle: `pnpm --filter frontend build` → анализ размера; убрать тяжёлые клиентские импорты из Server Components
- Добавить `loading.tsx` для основных роутов
- Добавить `error.tsx` для основных роутов
- Исправить критические находки; задокументировать в summary
- **Палитра по макетам:** обновить `frontend/src/app/globals.css` — задать акцентные и фоновые токены (OKLCH или hex → OKLCH) для светлой и тёмной темы; не добавлять `bg-blue-*` в компонентах; при необходимости подкрутить `chart-*`, sidebar-токены; кратко зафиксировать в summary ссылку на макеты/источник значений

#### Артефакты

- `frontend/src/app/globals.css` — палитра темы по макетам (семантические токены)
- `frontend/src/app/(app)/teacher/calendar/loading.tsx`
- `frontend/src/app/(app)/teacher/students/loading.tsx`
- `frontend/src/app/(app)/error.tsx`
- `frontend/src/app/(app)/not-found.tsx`

#### Definition of Done

**Агент:**

- [ ] Все Server Components не импортируют клиентские хуки или browser API
- [ ] `pnpm --filter frontend build` — нет TypeScript/ESLint ошибок
- [ ] `loading.tsx` добавлен для основных роутов
- [ ] Критические находки исправлены, задокументированы в summary
- [ ] Палитра из макетов отражена в теме (`globals.css`); новые экранные цвета не вводятся через raw Tailwind-классы

**Пользователь:**

- [ ] Запустить `make frontend-build` — сборка проходит без ошибок
- [ ] Открыть `/teacher/calendar` с медленной сетью (DevTools Throttling) — видна skeleton/loading UI
- [ ] Визуально сверить ключевые экраны с макетами (акцент, кнопки, фоны) в light и dark

#### Документы

- 📋 [План](impl/frontend/iteration-7-quality-review/tasks/task-23-code-review/plan.md)
- 📝 [Summary](impl/frontend/iteration-7-quality-review/tasks/task-23-code-review/summary.md)

---

## Итерация 8 — Тестирование 📋

### Цель

Актуализированы ручные тест-сценарии для 5 экранов; реализованы автотесты компонентов и API-клиента; работает `make frontend-test`.

### Документы итерации

- 📋 [План итерации](impl/frontend/iteration-8-testing/plan.md)
- 📝 [Summary итерации](impl/frontend/iteration-8-testing/summary.md)

---

### Задача 24: Тест-сценарии для 5 экранов 📋

#### Цель

Составлены ручные чек-листы для всех 5 экранов; зафиксированы в `docs/`.

#### Состав работ

- Описать сценарии для Экрана 1 (Вход): успешный вход teacher, успешный вход student, ошибочный пароль, редирект по роли
- Описать сценарии для Экрана 2 (Календарь): навигация по неделям, CRUD занятия, переключение флагов, кнопки напоминаний
- Описать сценарии для Экрана 3 (Ученики): переключение вид, CRUD ученика, детальная форма, лента диалога
- Описать сценарии для Экрана 4 (Настройки): заполнение формы, сохранение, сброс, валидация
- Описать сценарии для Экрана 5 (Расписание ученика): переключение вид, навигация, детали занятия
- Зафиксировать в `docs/tasks/impl/frontend/iteration-8-testing/tasks/task-24-test-scenarios/summary.md`

#### Артефакты

- `docs/tasks/impl/frontend/iteration-8-testing/tasks/task-24-test-scenarios/summary.md` — чек-листы

#### Definition of Done

**Агент:**

- [ ] Чек-листы составлены для всех 5 экранов
- [ ] Каждый сценарий содержит: предусловие, шаги, ожидаемый результат

**Пользователь:**

- [ ] Открыть summary задачи 24 — прочитать чек-листы
- [ ] Пройти ≥ 5 ключевых сценариев вручную

#### Документы

- 📋 [План](impl/frontend/iteration-8-testing/tasks/task-24-test-scenarios/plan.md)
- 📝 [Summary](impl/frontend/iteration-8-testing/tasks/task-24-test-scenarios/summary.md)

---

### Задача 25: Автотесты — unit и integration 📋

#### Цель

Реализованы автотесты ключевых компонентов и API-клиента; `make frontend-test` проходит.

#### Состав работ

- Установить `vitest` + `@testing-library/react` + `@testing-library/user-event` + `msw` в dev-зависимости frontend
- Настроить `frontend/vitest.config.ts` и `frontend/src/test/setup.ts`
- Написать unit-тесты:
  - `LessonCard`: отображение 5 флагов
  - `StudentCard`: отображение полей
  - `ThemeToggle`: переключение темы
- Написать integration-тесты с MSW-мок-сервером:
  - Форма входа: успешный вход → редирект
  - Форма настроек: загрузка данных, сохранение
- Обновить `Makefile`: цель `frontend-test` запускает `pnpm --filter frontend test`

#### Артефакты

- `frontend/vitest.config.ts`
- `frontend/src/test/setup.ts`
- `frontend/src/components/__tests__/lesson-card.test.tsx`
- `frontend/src/components/__tests__/student-card.test.tsx`
- `frontend/src/components/__tests__/theme-toggle.test.tsx`
- `frontend/src/app/__tests__/login.test.tsx`
- `frontend/src/app/__tests__/settings.test.tsx`
- `Makefile` — цель `frontend-test` обновлена

#### Definition of Done

**Агент:**

- [ ] `make frontend-test` проходит без ошибок
- [ ] Покрыты ≥ 5 unit-тестов и ≥ 2 integration-теста
- [ ] MSW-моки изолируют тесты от реального backend

**Пользователь:**

- [ ] Запустить `make frontend-test` — все тесты зелёные
- [ ] Запустить `make check` — линт и тесты проходят

#### Документы

- 📋 [План](impl/frontend/iteration-8-testing/tasks/task-25-automated-tests/plan.md)
- 📝 [Summary](impl/frontend/iteration-8-testing/tasks/task-25-automated-tests/summary.md)

---

## Makefile-цели frontend

| Цель | Команда | Добавляется в итерации |
|------|---------|----------------------|
| `frontend-dev` | `pnpm --filter frontend dev` | Итерация 2 |
| `frontend-build` | `pnpm --filter frontend build` | Итерация 2 |
| `frontend-lint` | `pnpm --filter frontend lint` | Итерация 2 |
| `frontend-test` | `pnpm --filter frontend test` | Итерация 8 |
| `check` (обновление) | добавить `frontend-lint` | Итерация 2 |

## Пробелы схемы данных (закрываются в Итерации 1)

| ID | Пробел | Решение |
|----|--------|---------|
| FG-01 | Нет 5 флагов статуса в `lessons` | Добавить `notification_sent`, `confirmed_by_student`, `homework_sent`, `solution_received`, `solution_checked` (boolean NOT NULL DEFAULT false) |
| FG-02 | Нет таблицы `reschedule_requests` | Создать: `id UUID PK`, `lesson_id UUID→lessons`, `student_id UUID→users`, `requested_at TIMESTAMPTZ`, `proposed_time TIMESTAMPTZ`, `status VARCHAR` (`pending`/`accepted`/`rejected`) |
| FG-03 | Нет таблицы `system_settings` | Создать: `key VARCHAR(64) PK`, `value TEXT NOT NULL` |
| FG-04 | Нет `password_hash` в `users` | Добавить `password_hash VARCHAR(255) NULL` (NULL у пользователей без веб-логина) |
