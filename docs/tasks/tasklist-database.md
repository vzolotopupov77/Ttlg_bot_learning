# Database Tasklist

## Обзор

Рабочий tasklist для внедрения полноценного слоя данных: от фиксации пользовательских сценариев и требований к данным — через проектирование и ревью схемы, документирование инструментов и инфраструктуру БД — до замены SQLite на PostgreSQL и верификации end-to-end.

Связь с дорожной картой: итерации 2 и 3 из [`docs/plan.md`](../plan.md) — конкретно часть «Проверка с PostgreSQL откладывается» и контекст из БД в реальном PostgreSQL.

## Легенда статусов

- 📋 Planned — Запланирован
- 🚧 In Progress — В работе
- ✅ Done — Завершён

---

## Сводная таблица задач

| № | Итерация | Описание | Статус | Документы |
|---|----------|----------|--------|-----------|
| 01 | 1 | Сценарии ученика | ✅ Done | [план](impl/database/iteration-1-user-scenarios/tasks/task-01-student-scenarios/plan.md) \| [summary](impl/database/iteration-1-user-scenarios/tasks/task-01-student-scenarios/summary.md) |
| 02 | 1 | Сценарии преподавателя + матрица данных | ✅ Done | [план](impl/database/iteration-1-user-scenarios/tasks/task-02-teacher-scenarios/plan.md) \| [summary](impl/database/iteration-1-user-scenarios/tasks/task-02-teacher-scenarios/summary.md) |
| 03 | 2 | Актуализация логической модели | ✅ Done | [план](impl/database/iteration-2-schema-design/tasks/task-03-logical-model/plan.md) \| [summary](impl/database/iteration-2-schema-design/tasks/task-03-logical-model/summary.md) |
| 04 | 2 | Физическая ER-диаграмма | ✅ Done | [план](impl/database/iteration-2-schema-design/tasks/task-04-physical-erd/plan.md) \| [summary](impl/database/iteration-2-schema-design/tasks/task-04-physical-erd/summary.md) |
| 05 | 2 | Ревью схемы через skill postgresql-table-design | ✅ Done | [план](impl/database/iteration-2-schema-design/tasks/task-05-schema-review/plan.md) \| [summary](impl/database/iteration-2-schema-design/tasks/task-05-schema-review/summary.md) |
| 06 | 3 | Ревью и актуализация ADR-002 | 📋 Planned | [план](impl/database/iteration-3-db-tooling/tasks/task-06-adr-review/plan.md) \| [summary](impl/database/iteration-3-db-tooling/tasks/task-06-adr-review/summary.md) |
| 07 | 3 | Практическая справка `docs/tech/db-guide.md` | 📋 Planned | [план](impl/database/iteration-3-db-tooling/tasks/task-07-db-guide/plan.md) \| [summary](impl/database/iteration-3-db-tooling/tasks/task-07-db-guide/summary.md) |
| 08 | 4 | Недостающие make-цели (reset, shell, logs) | 📋 Planned | [план](impl/database/iteration-4-db-infra/tasks/task-08-make-targets/plan.md) \| [summary](impl/database/iteration-4-db-infra/tasks/task-08-make-targets/summary.md) |
| 09 | 4 | Seed-скрипт и цель `make backend-db-seed` | 📋 Planned | [план](impl/database/iteration-4-db-infra/tasks/task-09-seed/plan.md) \| [summary](impl/database/iteration-4-db-infra/tasks/task-09-seed/summary.md) |
| 10 | 4 | Команды просмотра данных и SQL-сниппеты | 📋 Planned | [план](impl/database/iteration-4-db-infra/tasks/task-10-inspection/plan.md) \| [summary](impl/database/iteration-4-db-infra/tasks/task-10-inspection/summary.md) |
| 11 | 5 | Актуализация ORM-моделей | 📋 Planned | [план](impl/database/iteration-5-orm-integration/tasks/task-11-orm-models/plan.md) \| [summary](impl/database/iteration-5-orm-integration/tasks/task-11-orm-models/summary.md) |
| 12 | 5 | Ревью и доработка репозиториев | 📋 Planned | [план](impl/database/iteration-5-orm-integration/tasks/task-12-repositories/plan.md) \| [summary](impl/database/iteration-5-orm-integration/tasks/task-12-repositories/summary.md) |
| 13 | 5 | Тестовый стенд с PostgreSQL | 📋 Planned | [план](impl/database/iteration-5-orm-integration/tasks/task-13-pg-test-harness/plan.md) \| [summary](impl/database/iteration-5-orm-integration/tasks/task-13-pg-test-harness/summary.md) |
| 14 | 5 | End-to-end smoke на PostgreSQL + документация | 📋 Planned | [план](impl/database/iteration-5-orm-integration/tasks/task-14-e2e-smoke/plan.md) \| [summary](impl/database/iteration-5-orm-integration/tasks/task-14-e2e-smoke/summary.md) |

---

## Итерация 1 — Сценарии пользователя и требования к данным

**Цель:** зафиксировать, что ученик и преподаватель видят и делают в базовых сценариях — без технических деталей. Результат служит основой для проектирования схемы, frontend и понимания того, какие сущности, поля и связи точно понадобятся.

**Ценность:** после этой итерации видно, какие агрегации, запросы и состояния должна поддерживать схема — до написания первой миграции.

**Артефакты:** `docs/tech/user-scenarios.md`

**Документы итерации:** [план](impl/database/iteration-1-user-scenarios/plan.md) | [summary](impl/database/iteration-1-user-scenarios/summary.md)

---

### Задача 01: Сценарии ученика ✅

#### Цель

Описать 5–7 базовых сценариев взаимодействия ученика с системой: что он видит, что делает, какой результат ожидает. Без технических деталей реализации — только с точки зрения пользователя.

#### Состав работ

- Выделить сценарии из [`docs/vision.md`](../vision.md) и [`docs/idea.md`](../idea.md): расписание, ДЗ, диалог с ассистентом, прогресс, напоминания
- Для каждого сценария: название, краткое описание, шаги, ожидаемый результат, канал (бот / веб)
- Указать, какие данные из БД нужны для отображения каждого сценария (сущности, поля — без SQL)
- Зафиксировать в `docs/tech/user-scenarios.md` раздел «Ученик»

#### Артефакты

- `docs/tech/user-scenarios.md` — раздел «Ученик»

#### Definition of Done

**Агент:**

- Описаны минимум 5 сценариев ученика; каждый содержит: шаги, ожидаемый результат, канал
- Для каждого сценария явно указаны требуемые сущности (не SQL, а логические имена: `User`, `Lesson`, `Assignment` и т.д.)
- Нет противоречий с [`docs/vision.md`](../vision.md) — каналы и роли совпадают

**Пользователь:**

- Открыть `docs/tech/user-scenarios.md` → прочитать сценарии ученика → убедиться, что они узнаваемы и отражают реальный опыт использования
- Проверить: нет ли важного сценария, который пропущен (например «получить ответ от ассистента», «посмотреть прогресс»)

#### Документы

- 📋 [План](impl/database/iteration-1-user-scenarios/tasks/task-01-student-scenarios/plan.md)
- 📝 [Summary](impl/database/iteration-1-user-scenarios/tasks/task-01-student-scenarios/summary.md)

---

### Задача 02: Сценарии преподавателя + матрица данных ✅

#### Цель

Описать 5–7 базовых сценариев преподавателя и построить матрицу «сценарий → данные», которая покажет, какие сущности, поля и связи точно понадобятся — в том числе неочевидные (например: преподаватель видит прогресс ученика → нужен `Progress` + агрегации по `Assignment` и `Lesson`).

#### Состав работ

- Описать сценарии преподавателя в `docs/tech/user-scenarios.md` раздел «Преподаватель» (управление расписанием, ДЗ, просмотр прогресса, база материалов)
- Построить сводную матрицу: строки — сценарии, столбцы — сущности; отметить задействованные поля
- Выявить и зафиксировать пробелы: что есть в сценариях, но отсутствует или не детализировано в [`docs/data-model.md`](../data-model.md)
- Дать рекомендации по изменениям схемы (если выявлены) — без реализации, только фиксация

#### Артефакты

- `docs/tech/user-scenarios.md` — раздел «Преподаватель» + матрица данных

#### Definition of Done

**Агент:**

- Описаны минимум 5 сценариев преподавателя с шагами и ожидаемыми результатами
- Матрица заполнена: каждый сценарий сопоставлен с задействованными сущностями и ключевыми полями
- Явно указаны пробелы или расхождения с текущей схемой (даже если их нет — это подтверждено явно)
- Сценарии не противоречат [`docs/vision.md`](../vision.md)

**Пользователь:**

- Открыть матрицу данных → убедиться, что для каждого важного сценария есть понятная привязка к данным
- Проверить: покрывает ли текущая схема все сценарии, или нужны доработки?

#### Документы

- 📋 [План](impl/database/iteration-1-user-scenarios/tasks/task-02-teacher-scenarios/plan.md)
- 📝 [Summary](impl/database/iteration-1-user-scenarios/tasks/task-02-teacher-scenarios/summary.md)

### Проверка итерации 1

**Агент:** `docs/tech/user-scenarios.md` существует; охвачены обе роли; матрица данных заполнена; выявленные пробелы зафиксированы в summary итерации.

**Пользователь:** прочитать `docs/tech/user-scenarios.md` целиком — понятно, что должна уметь система и какие данные для этого нужны.

---

## Итерация 2 — Проектирование схемы данных

**Цель:** актуализировать логическую модель в [`docs/data-model.md`](../data-model.md) с учётом сценариев из итерации 1; нарисовать физическую ER-диаграмму с типами, constraints и индексами; провести ревью схемы через skill `postgresql-table-design` и зафиксировать принятые решения.

**Ценность:** после итерации есть единый актуальный источник правды по схеме, пригодный для ревью кода, онбординга и работы с frontend-командой.

**Артефакты:** обновлённый `docs/data-model.md` с физической ERD; при необходимости — обновлённый `docs/adr/adr-001-database.md`

**Документы итерации:** [план](impl/database/iteration-2-schema-design/plan.md) | [summary](impl/database/iteration-2-schema-design/summary.md)

---

### Задача 03: Актуализация логической модели ✅

#### Цель

Привести логическую модель в [`docs/data-model.md`](../data-model.md) в соответствие с реализованными ORM-моделями (`storage/models.py`) и с требованиями, выявленными в итерации 1. Устранить расхождения между документом и кодом.

#### Состав работ

- Сверить таблицы, поля и типы в [`docs/data-model.md`](../data-model.md) с [`backend/src/ttlg_backend/storage/models.py`](../../backend/src/ttlg_backend/storage/models.py)
- Актуализировать: тип PK (UUID — уже принято в summary задачи 10 основного tasklist), nullable поля, enum-значения
- Добавить поля, выявленные при анализе сценариев (задача 02), если они отсутствуют
- Обновить текстовые описания сущностей (секции «Поле / Тип / Описание»)

#### Артефакты

- `docs/data-model.md` — обновлённые таблицы сущностей

#### Definition of Done

**Агент:**

- Каждое поле в документе соответствует колонке в ORM-модели: имя, тип (логический), nullable
- Enum-значения в документе совпадают с `StrEnum` в `models.py`
- PK всех сущностей задокументированы как UUID (не int)
- Зафиксированы расхождения с предыдущей версией документа в summary задачи

**Пользователь:**

- Открыть `docs/data-model.md` → сравнить с `storage/models.py` → не найти расхождений в типах и полях

#### Документы

- 📋 [План](impl/database/iteration-2-schema-design/tasks/task-03-logical-model/plan.md)
- 📝 [Summary](impl/database/iteration-2-schema-design/tasks/task-03-logical-model/summary.md)

---

### Задача 04: Физическая ER-диаграмма ✅

#### Цель

Добавить в [`docs/data-model.md`](../data-model.md) физическую ER-диаграмму: типы колонок PostgreSQL, nullable, constraints (PK, FK, UNIQUE), каскады (`ON DELETE CASCADE / SET NULL`), ключевые индексы. Диаграмма должна давать достаточно информации для ревью и работы с `psql`.

#### Состав работ

- Построить физическую ERD в Mermaid (`erDiagram`) на основе `storage/models.py` и принятых решений
- Указать в аннотациях к каждой сущности: PostgreSQL-тип колонок (UUID, BIGINT, VARCHAR, TEXT, DATE, TIMESTAMPTZ, enum-тип), nullable/NOT NULL
- Добавить секцию «Физическая схема» в `docs/data-model.md` отдельно от логической ERD
- Задокументировать каскады FK и ключевые индексы в виде отдельной таблицы или списка под диаграммой

#### Артефакты

- `docs/data-model.md` — новая секция «Физическая схема» с ERD и таблицей constraints/индексов

#### Definition of Done

**Агент:**

- ERD содержит все 6 сущностей: `users`, `lessons`, `assignments`, `progress`, `dialogues`, `messages`
- Для каждой колонки указан PostgreSQL-тип и nullable
- FK каскады (`CASCADE`, `SET NULL`) указаны явно и соответствуют `models.py`
- Ключевые индексы (`student_id`, `teacher_id`, `dialogue_id`, `telegram_id UNIQUE`) перечислены

**Пользователь:**

- Открыть секцию «Физическая схема» → запустить `make backend-db-shell` → выполнить `\d lessons` → типы колонок совпадают с диаграммой

#### Документы

- 📋 [План](impl/database/iteration-2-schema-design/tasks/task-04-physical-erd/plan.md)
- 📝 [Summary](impl/database/iteration-2-schema-design/tasks/task-04-physical-erd/summary.md)

---

### Задача 05: Ревью схемы через skill `postgresql-table-design` ✅

#### Цель

Применить skill `postgresql-table-design` к текущей схеме; зафиксировать рекомендации, принятые решения и обоснованные отклонения. При необходимости обновить `docs/data-model.md` и `docs/adr/adr-001-database.md`.

#### Состав работ

- Прочитать skill `postgresql-table-design` и применить его чек-лист к физической схеме из задачи 04
- Отработать категории: типы данных (timestamptz vs timestamp, UUID vs serial), именование, индексы, constraints, NULL-семантика, нормализация
- Для каждой рекомендации: принять (с фиксацией в `data-model.md`) или отклонить (с обоснованием в summary)
- Если выявлены изменения схемы — создать новую Alembic-ревизию (или отложить до задачи 11 итерации 5 с явной пометкой)

#### Артефакты

- `docs/data-model.md` — дополнена принятыми решениями по типам/индексам
- `docs/adr/adr-001-database.md` — при необходимости обновлены последствия
- summary задачи: таблица «Рекомендация → Решение → Обоснование»

#### Definition of Done

**Агент:**

- Каждая рекомендация skill отработана: принята или явно отклонена с обоснованием
- Все `DateTime` → `TIMESTAMPTZ` (уже в моделях; подтверждено)
- Индексы для FK-колонок с частыми запросами (`student_id`, `dialogue_id`) — подтверждены или добавлены
- Нет непроверенных пунктов чек-листа skill

**Пользователь:**

- Открыть summary задачи 05 → прочитать таблицу решений → понять, почему схема выглядит именно так

#### Документы

- 📋 [План](impl/database/iteration-2-schema-design/tasks/task-05-schema-review/plan.md)
- 📝 [Summary](impl/database/iteration-2-schema-design/tasks/task-05-schema-review/summary.md)

### Проверка итерации 2

**Агент:** `docs/data-model.md` содержит физическую ERD; все рекомендации skill обработаны; расхождения между документом и кодом устранены.

**Пользователь:** открыть `docs/data-model.md` → физическая ERD читаема; открыть `make backend-db-shell` → `\d+ users` → схема соответствует диаграмме.

---

## Итерация 3 — Инструменты: документирование и практическая справка

**Цель:** убедиться, что ADR-002 актуален, и создать практическую how-to справку по работе с БД в проекте — для агентов и разработчиков.

**Ценность:** после итерации любой участник может без поиска по коду понять, как добавить таблицу, создать миграцию, написать репозиторий.

**Артефакты:** `docs/tech/db-guide.md`; при необходимости — обновлённый `docs/adr/adr-002-orm-migrations-tests.md`

**Документы итерации:** [план](impl/database/iteration-3-db-tooling/plan.md) | [summary](impl/database/iteration-3-db-tooling/summary.md)

---

### Задача 06: Ревью и актуализация ADR-002 📋

#### Цель

Проверить, что [`docs/adr/adr-002-orm-migrations-tests.md`](../adr/adr-002-orm-migrations-tests.md) отражает фактически принятые решения: SQLAlchemy async, Alembic, asyncpg, UUID PK, async-enum (StrEnum + `native_enum=True`), тестовая изоляция. При необходимости обновить секцию «Последствия».

#### Состав работ

- Сверить ADR-002 с реализацией: `storage/models.py`, `backend/alembic/`, `backend/pyproject.toml`
- Зафиксировать конкретные решения, принятые в ходе реализации: UUID PK (не int), `StrEnum` + `native_enum=True`, `asyncpg`, `asyncio_mode=auto` в pytest
- Если реализация расходится с ADR — обновить ADR или добавить новую запись в журнал (`docs/adr/README.md`)
- Обновить дату и статус ADR если вносились изменения

#### Артефакты

- `docs/adr/adr-002-orm-migrations-tests.md` — при необходимости обновлены секции «Решение» и «Последствия»

#### Definition of Done

**Агент:**

- ADR-002 соответствует коду: UUID PK, StrEnum, asyncpg, asyncio_mode — упомянуты явно
- Нет устаревших пунктов (например ссылок на SQLite как основную тестовую БД — только как временное решение, которое заменяется в итерации 5)
- Если вносились изменения — дата ADR обновлена

**Пользователь:**

- Прочитать ADR-002 → понять, почему выбраны SQLAlchemy async + Alembic, и в чём особенности текущей реализации (UUID PK, StrEnum)

#### Документы

- 📋 [План](impl/database/iteration-3-db-tooling/tasks/task-06-adr-review/plan.md)
- 📝 [Summary](impl/database/iteration-3-db-tooling/tasks/task-06-adr-review/summary.md)

---

### Задача 07: Практическая справка `docs/tech/db-guide.md` 📋

#### Цель

Создать практическую справку по работе с БД в проекте: как устроен доступ к данным, как создать и применить миграцию, как написать репозиторий, какие Makefile-команды использовать. Документ — для агентов и разработчиков, не дублирует ADR.

#### Состав работ

- Описать структуру слоя данных: `storage/models.py`, `storage/repositories/`, `db.py`, `dependencies.py`
- Написать раздел «Миграции»: как создать новую ревизию (`alembic revision --autogenerate`), проверить, применить, откатить; соответствующие make-цели
- Написать раздел «Репозитории»: паттерн (AsyncSession, методы create/get/list/update), типовой шаблон нового репозитория
- Написать раздел «Сессия в FastAPI»: как `AsyncSession` инжектируется через `Depends`, цикл жизни
- Добавить 5 типовых SQL-сниппетов для разработчика (через `make backend-db-shell`): список пользователей, занятия ученика, ДЗ со статусом, диалоги, последние сообщения

#### Артефакты

- `docs/tech/db-guide.md` — новый файл

#### Definition of Done

**Агент:**

- Справка содержит 4 раздела: структура слоя, миграции, репозитории, сессия в FastAPI
- Все make-команды в справке существуют в `Makefile` (на момент итерации 4 — после задачи 08)
- 5 SQL-сниппетов проверены на работающей БД
- Нет ссылок на несуществующие файлы

**Пользователь:**

- По справке выполнить: `alembic revision --autogenerate -m "test"` → убедиться, что файл создан → `alembic downgrade -1` → удалить файл; всё — без дополнительного поиска команд
- Пробежать по SQL-сниппетам в `make backend-db-shell` → все работают

#### Документы

- 📋 [План](impl/database/iteration-3-db-tooling/tasks/task-07-db-guide/plan.md)
- 📝 [Summary](impl/database/iteration-3-db-tooling/tasks/task-07-db-guide/summary.md)

### Проверка итерации 3

**Агент:** `docs/tech/db-guide.md` создан; ADR-002 актуален; все команды в справке проверены.

**Пользователь:** открыть `docs/tech/db-guide.md` → пройти раздел «Миграции» шаг за шагом.

---

## Итерация 4 — Инфраструктура БД

**Цель:** добавить недостающие Makefile-цели для локальной разработки (сброс, psql-шелл, логи), создать seed-скрипт с тестовыми данными и задокументировать типовые команды просмотра.

**Ценность:** после итерации разработчик одной командой поднимает чистое окружение с тестовыми данными и может инспектировать состояние БД без дополнительной настройки.

**Артефакты:** обновлённый `Makefile`, `backend/scripts/seed.py`, дополнение в `docs/tech/db-guide.md`

**Документы итерации:** [план](impl/database/iteration-4-db-infra/plan.md) | [summary](impl/database/iteration-4-db-infra/summary.md)

---

### Задача 08: Недостающие make-цели 📋

#### Цель

Добавить в `Makefile` цели, необходимые для полного цикла локальной работы с БД: пересоздание окружения, интерактивный шелл, просмотр логов контейнера.

#### Состав работ

- `backend-db-reset` — остановить контейнер, удалить volume, поднять заново, применить миграции; аналог «начать с чистого листа»
- `backend-db-shell` — открыть `psql` внутри контейнера `db` с реквизитами из `docker-compose.yml`
- `backend-db-logs` — `docker compose logs -f db`
- Добавить новые цели в `.PHONY` и обновить `docs/tech/db-guide.md` (раздел «Makefile-цели»)

#### Артефакты

- `Makefile` — 3 новые цели
- `docs/tech/db-guide.md` — обновлён раздел с командами

#### Definition of Done

**Агент:**

- `make backend-db-reset` выполняется без ошибок на чистом окружении; после него `make backend-db-migrate` применяет миграции с нуля
- `make backend-db-shell` открывает `psql` и `\dt` показывает таблицы после миграции
- `make backend-db-logs` выводит логи PostgreSQL без ошибок
- Все 3 цели добавлены в `.PHONY`

**Пользователь:**

- `make backend-db-reset` → `make backend-db-migrate` → `make backend-db-shell` → `\dt` → список таблиц виден
- `make backend-db-logs` → в выводе видны строки о готовности PostgreSQL

#### Документы

- 📋 [План](impl/database/iteration-4-db-infra/tasks/task-08-make-targets/plan.md)
- 📝 [Summary](impl/database/iteration-4-db-infra/tasks/task-08-make-targets/summary.md)

---

### Задача 09: Seed-скрипт и `make backend-db-seed` 📋

#### Цель

Создать скрипт тестового наполнения БД: один преподаватель, один ученик с известным `telegram_id`, одно занятие, одно ДЗ. Данные идемпотентны — повторный запуск не создаёт дублей.

#### Состав работ

- Создать `backend/scripts/seed.py` — async-скрипт, использующий ORM-модели и `AsyncSession`
- Данные: `teacher` (role=teacher, name="Преподаватель"), `student` (role=student, name="Ученик", telegram_id=из `.env` или константа для dev), `Lesson` (статус scheduled, дата в будущем), `Assignment` (статус pending, due_date через неделю)
- Идемпотентность: проверять наличие записи перед вставкой (по telegram_id / имени); не падать при повторном запуске
- Добавить цель `backend-db-seed` в `Makefile`

#### Артефакты

- `backend/scripts/seed.py`
- `Makefile` — цель `backend-db-seed`

#### Definition of Done

**Агент:**

- `make backend-db-seed` выполняется без ошибок на чистой (после reset+migrate) БД
- Повторный `make backend-db-seed` завершается успешно и не создаёт дублей
- Скрипт использует только ORM-модели и `AsyncSession`; нет raw SQL
- Значения `telegram_id` ученика задокументированы в комментарии к скрипту и в `docs/tech/db-guide.md`

**Пользователь:**

- `make backend-db-reset && make backend-db-migrate && make backend-db-seed`
- `make backend-db-shell` → `SELECT name, role FROM users;` → 2 строки (teacher + student)
- Повторный `make backend-db-seed` → сообщение «already seeded» или тихий выход; `SELECT count(*) FROM users;` → всё ещё 2

#### Документы

- 📋 [План](impl/database/iteration-4-db-infra/tasks/task-09-seed/plan.md)
- 📝 [Summary](impl/database/iteration-4-db-infra/tasks/task-09-seed/summary.md)

---

### Задача 10: Команды просмотра данных и SQL-сниппеты 📋

#### Цель

Задокументировать типовые команды для инспекции состояния БД во время разработки. Добавить в `docs/tech/db-guide.md` раздел «Просмотр данных» с готовыми SQL-запросами.

#### Состав работ

- Написать 5 SQL-сниппетов для `make backend-db-shell`:
  1. Все пользователи с ролями
  2. Занятия конкретного ученика (с teacher_id и статусом)
  3. ДЗ с просроченным дедлайном
  4. Последние 10 сообщений в диалогах
  5. Прогресс по всем ученикам за текущий период
- Добавить в `docs/tech/db-guide.md` раздел «Просмотр данных» со сниппетами
- Проверить каждый запрос на seed-данных из задачи 09

#### Артефакты

- `docs/tech/db-guide.md` — раздел «Просмотр данных»

#### Definition of Done

**Агент:**

- 5 сниппетов работают без ошибок на БД после `make backend-db-seed`
- Каждый сниппет содержит однострочный комментарий о назначении
- Раздел добавлен в `docs/tech/db-guide.md`

**Пользователь:**

- `make backend-db-shell` → скопировать любой из 5 сниппетов → выполнить → получить результат без ошибок

#### Документы

- 📋 [План](impl/database/iteration-4-db-infra/tasks/task-10-inspection/plan.md)
- 📝 [Summary](impl/database/iteration-4-db-infra/tasks/task-10-inspection/summary.md)

### Проверка итерации 4

**Агент:** `make backend-db-reset && make backend-db-migrate && make backend-db-seed` — без ошибок; `make backend-db-shell` работает; все новые цели в `.PHONY`; SQL-сниппеты в `db-guide.md` проверены.

**Пользователь:**

```text
make backend-db-reset
make backend-db-migrate
make backend-db-seed
make backend-db-shell
```

В `psql`: `SELECT name, role FROM users;` → 2 строки. `\dt` → все таблицы.

---

## Итерация 5 — ORM, репозитории, интеграция в backend

**Цель:** привести ORM-модели и репозитории в соответствие с итогами ревью схемы; настроить тесты против PostgreSQL; верифицировать полный сценарий end-to-end на PostgreSQL.

**Ценность:** после итерации backend полностью работает на PostgreSQL — без SQLite-заглушки; тесты гарантируют отсутствие регрессий при изменении схемы.

**Артефакты:** обновлённый `storage/models.py`, новая Alembic-ревизия (если нужна), обновлённые фикстуры тестов, обновлённая документация

**Документы итерации:** [план](impl/database/iteration-5-orm-integration/plan.md) | [summary](impl/database/iteration-5-orm-integration/summary.md)

---

### Задача 11: Актуализация ORM-моделей 📋

#### Цель

Применить решения из задачи 05 (ревью схемы): скорректировать типы, добавить индексы, уточнить nullable — если итоги ревью требуют изменений. Создать новую Alembic-ревизию при изменении схемы.

#### Состав работ

- Применить конкретные изменения из summary задачи 05 (если есть) к [`backend/src/ttlg_backend/storage/models.py`](../../backend/src/ttlg_backend/storage/models.py)
- Сгенерировать и проверить Alembic-ревизию: `alembic revision --autogenerate -m "schema_review_fixes"` — если изменений нет, явно подтвердить в summary
- Применить ревизию на чистой БД: `make backend-db-reset && make backend-db-migrate`
- Если изменений схемы нет — задача сводится к подтверждению корректности и закрытию пунктов из задачи 05

#### Артефакты

- `backend/src/ttlg_backend/storage/models.py` — при необходимости обновлён
- `backend/alembic/versions/` — новая ревизия при изменениях схемы

#### Definition of Done

**Агент:**

- `make backend-db-reset && make backend-db-migrate` — без ошибок
- `make backend-test` (с SQLite) — не сломан: 17 passed
- Все изменения из задачи 05 применены или явно отклонены с обоснованием в summary

**Пользователь:**

- `make backend-db-shell` → `\d+ users` → схема совпадает с физической ERD из задачи 04
- `make backend-test` → зелёный

#### Документы

- 📋 [План](impl/database/iteration-5-orm-integration/tasks/task-11-orm-models/plan.md)
- 📝 [Summary](impl/database/iteration-5-orm-integration/tasks/task-11-orm-models/summary.md)

---

### Задача 12: Ревью и доработка репозиториев 📋

**Skill:** перед началом прочитать skill `fastapi-templates` и применить его паттерны к слою репозиториев и dependency injection.

#### Цель

Проверить репозитории в `storage/repositories/` на полноту методов, корректность async-паттернов и обработку граничных случаев (`None`, пустые результаты). Привести к единому стилю, согласованному с паттернами FastAPI dependency injection из skill.

#### Состав работ

- Прочитать skill `fastapi-templates`; выписать релевантные паттерны: репозитории через `Depends`, сессия через `AsyncSession`, структура слоя доступа к данным
- Пройти по каждому репозиторию (`users`, `lessons`, `assignments`, `dialogues`, `progress_summary`) и проверить:
  - Наличие методов `get_by_id`, `list` (с фильтрами где нужно), `create`
  - Корректная обработка `None` при `get_by_id` (не бросать исключение внутри репозитория)
  - Нет `session.execute(select(...)).all()` с `scalars()` перепутанными
  - Нет утечки `session` за пределы вызова
  - Инъекция сессии через `Depends` соответствует паттерну skill (не создаётся внутри репозитория)
- Устранить найденные проблемы; задокументировать принятый паттерн в `docs/tech/db-guide.md`

#### Артефакты

- `backend/src/ttlg_backend/storage/repositories/*.py` — при необходимости обновлены
- `docs/tech/db-guide.md` — раздел «Репозитории» дополнен по итогам ревью и skill

#### Definition of Done

**Агент:**

- Паттерны skill `fastapi-templates` применены или явно отклонены с обоснованием в summary
- Каждый репозиторий проверен; найденные проблемы устранены или явно задокументированы как accepted risk
- `make backend-test` — 17 passed (регрессий нет)
- `make lint` — без ошибок

**Пользователь:**

- `make backend-test` → зелёный
- `make lint` → чисто

#### Документы

- 📋 [План](impl/database/iteration-5-orm-integration/tasks/task-12-repositories/plan.md)
- 📝 [Summary](impl/database/iteration-5-orm-integration/tasks/task-12-repositories/summary.md)

---

### Задача 13: Тестовый стенд с PostgreSQL 📋

**Skill:** перед реализацией фикстур прочитать skill `python-testing-patterns` и применить его рекомендации по async-фикстурам, изоляции БД и организации `conftest.py`. Если в ходе задачи или задачи 14 появляются дополнительные тестовые сценарии (репозитории, граничные случаи, параметризованные кейсы) — применить паттерны skill для их оформления.

#### Цель

Настроить тесты backend так, чтобы `make backend-test` работал против реального PostgreSQL — без `TTLG_ALLOW_SQLITE_TEST=1`. Выбрать подход к изоляции (тестовая БД + транзакция с откатом или `testcontainers`), реализовать фикстуры согласно паттернам skill.

#### Состав работ

- Прочитать skill `python-testing-patterns`; выписать паттерны для async-тестов с реальной БД: фикстуры с `scope`, транзакционная изоляция, фабрики тестовых данных
- Определить подход к тестовой БД: отдельная база `ttlg_test` в запущенном контейнере или `testcontainers-python` для автозапуска; зафиксировать в summary
- Реализовать фикстуры: `engine` (async), `session` (с откатом транзакции после теста), `client` (ASGI + тестовая сессия) — по паттернам skill
- Если выявлены непокрытые сценарии репозиториев или граничные случаи — добавить тесты с использованием паттернов skill (параметризация, фабрики данных, маркеры)
- Убрать или сделать опциональным `TTLG_ALLOW_SQLITE_TEST`; обновить `backend/pyproject.toml` (dev-зависимости), `.env.example`, `docs/tech/db-guide.md`
- Добавить цель `backend-db-test-up` (если нужна отдельная тестовая БД) или обновить `backend-db-up` под оба сценария

#### Артефакты

- `backend/tests/conftest.py` — обновлённые фикстуры
- `backend/pyproject.toml` — при необходимости новые dev-зависимости
- `.env.example` — при необходимости `DATABASE_TEST_URL` или инструкция
- `docs/tech/db-guide.md` — раздел «Тесты с PostgreSQL»
- `Makefile` — при необходимости новая цель

#### Definition of Done

**Агент:**

- Паттерны skill `python-testing-patterns` применены к фикстурам; отклонения обоснованы в summary
- `make backend-test` — все тесты passed против PostgreSQL без `TTLG_ALLOW_SQLITE_TEST`
- Каждый тест изолирован: данные одного теста не видны другому
- Нет `aiosqlite` / `sqlite` в тестовых зависимостях (или явно помечены как более не нужные)
- Если добавлены новые тесты — они оформлены по паттернам skill (scope фикстур, маркеры, параметризация где уместно)

**Пользователь:**

- Поднять PostgreSQL: `make backend-db-up`
- `make backend-test` → все зелёные
- Убедиться, что тесты не оставляют мусорных данных: `make backend-db-shell` → `SELECT count(*) FROM users;` → 0 (или только seed если он запускался отдельно)

#### Документы

- 📋 [План](impl/database/iteration-5-orm-integration/tasks/task-13-pg-test-harness/plan.md)
- 📝 [Summary](impl/database/iteration-5-orm-integration/tasks/task-13-pg-test-harness/summary.md)

---

### Задача 14: End-to-end smoke на PostgreSQL + документация 📋

#### Цель

Верифицировать полный сценарий на PostgreSQL: поднять БД, накатить миграции, загрузить seed-данные, запустить backend, выполнить запрос с реальным `telegram_id` ученика — получить ответ и убедиться в сохранении в PostgreSQL. Обновить документацию.

#### Состав работ

- Выполнить полный сценарий: `make backend-db-reset && make backend-db-migrate && make backend-db-seed && make backend-run`
- Отправить `POST /v1/dialogue/message` с `telegram_id` seed-ученика → получить ответ → проверить в `psql`: `SELECT * FROM messages ORDER BY created_at DESC LIMIT 5;`
- Обновить [`docs/data-model.md`](../data-model.md) если схема изменилась в задаче 11
- Обновить [`README.md`](../../README.md): заменить SQLite-маршрут запуска на PostgreSQL; SQLite-вариант — опциональный (например в отдельном разделе или с пометкой «только для быстрого старта без БД»)
- Обновить [`docs/vision.md`](../vision.md): снять пометку «без PostgreSQL» в таблице технологий и описании слоя данных, если она ещё есть
- Обновить `docs/plan.md`: статус части Итерации 2 («Проверка с PostgreSQL») — Done

#### Артефакты

- Обновлённые: `README.md`, `docs/data-model.md` (при необходимости), `docs/vision.md` (при необходимости), `docs/plan.md`
- Обновлённый `smoke-integration` в `Makefile`: шаги должны включать PostgreSQL-путь

#### Definition of Done

**Агент:**

- `make backend-test` — зелёный (против PostgreSQL)
- `make check` — lint + оба набора тестов — зелёный
- README содержит PostgreSQL-маршрут запуска как основной
- `docs/plan.md` — Итерация 2 помечена ✅ Done по части PostgreSQL

**Пользователь:**

- Выполнить по README шаги для PostgreSQL-режима с нуля — без обращения к другим документам
- `POST /v1/dialogue/message` с seed-`telegram_id` → ответ получен
- `make backend-db-shell` → `SELECT role, content FROM messages ORDER BY created_at DESC LIMIT 2;` → видны user + assistant сообщения

#### Документы

- 📋 [План](impl/database/iteration-5-orm-integration/tasks/task-14-e2e-smoke/plan.md)
- 📝 [Summary](impl/database/iteration-5-orm-integration/tasks/task-14-e2e-smoke/summary.md)

### Проверка итерации 5

**Агент:**

- `make backend-test` — зелёный против PostgreSQL; без `TTLG_ALLOW_SQLITE_TEST`
- `make check` — lint + все тесты — зелёный
- `make backend-db-reset && make backend-db-migrate && make backend-db-seed` — без ошибок
- README, vision, plan.md актуальны

**Пользователь:**

```text
make backend-db-reset
make backend-db-migrate
make backend-db-seed
make backend-run   # терминал 1
make run           # терминал 2
```

Telegram: `/start` и вопрос → ответ из backend. `make backend-db-shell` → `SELECT * FROM messages LIMIT 5;` → сообщения сохранены в PostgreSQL.

---

## Дальнейшие итерации (вне scope этого tasklist)

| Тема | Документ |
|------|----------|
| Расписание, ДЗ, напоминания | [tasklist-backend-iteration-4-schedule-hw.md](tasklist-backend-iteration-4-schedule-hw.md) |
| Прогресс и аналитика | [tasklist-backend-iteration-6-progress.md](tasklist-backend-iteration-6-progress.md) |
| Веб-интерфейс | [tasklist-frontend-iteration-5-web.md](tasklist-frontend-iteration-5-web.md) |

При появлении новых команд обслуживания БД — обновлять `Makefile` и `docs/tech/db-guide.md`.
