# Итерация 1 — Реализация API для frontend: summary

## Результат

Реализованы миграции схемы (флаги занятий, `password_hash`/`notes` у пользователей, `reschedule_requests`, `system_settings`), JWT-аутентификация (bcrypt + HS256, cookie `ttlg_access_token` и заголовок `Authorization: Bearer`), роутеры `auth`, `teacher`, `students`, `settings`, `student`, расширен `lessons` (PUT, DELETE, PATCH `/flags`). Добавлены seed-миграции: mock-данные и преподаватель Владимир (`vzolotoy@mail.ru`). Обновлены `docs/data-model.md`, `.env.example`, `Makefile` (openapi-export с `SECRET_KEY`).

## Отклонения от плана

- Хеширование паролей: библиотека `bcrypt` напрямую (вместо `passlib`) — совместимость с bcrypt 5.x и миграциями Alembic.
- Обработчик `HTTPException` в `main.py` — единый JSON `{"error":{code,message}}` для 401/403/404 из зависимостей.

## Проблемы / решения

- Alembic + `text()`: конструкция `:id::uuid` ломала разбор параметров; заменено на `CAST(:id AS uuid)`.
- Seed преподавателя: `passlib` + bcrypt 5 вызывал ошибку в миграции; хеш в миграции через `bcrypt.hashpw`.

## Проверки

- `make backend-test` — 22 теста (в т.ч. `test_auth_and_teacher.py`).
- `alembic upgrade head` — применено на dev-БД.

---

## Зафиксированные результаты проверок (2026-04-12)

Сверка с навыками **modern-python** и **fastapi-templates** (см. `.agents/skills/`).

### Инструменты (modern-python)

| Проверка | Команда | Результат |
|----------|---------|-----------|
| Линтер | `uv run ruff check backend/src backend/tests` | Успешно |
| Формат | `uv run ruff format backend/src backend/tests` | После проверки отформатирован `storage/repositories/dialogues.py` (был расхождение с `ruff format`) |
| Тесты | `uv run --package ttlg-backend pytest backend/tests` | 22 passed |
| Зависимости | `backend/pyproject.toml` | Runtime в `[project]`, dev в `[dependency-groups] dev` — без `[project.optional-dependencies]` для dev |

**Не внедрялось в этом цикле:** статический анализатор **ty** (skill рекомендует `ty check`; в backend-пакете нет цели в Makefile — опционально).

### Архитектура (fastapi-templates)

| Критерий | Статус |
|----------|--------|
| Роутеры по доменам в `api/` | Соответствует |
| `Depends(get_session)`, JWT в `api/deps.py` | Соответствует |
| Репозитории в `storage/repositories/` | Соответствует |
| `services/auth_service.py` (JWT, bcrypt) | Соответствует |
| Толстый service-слой для teacher/students | Частично: логика в роутерах + репозитории (KISS по конвенциям проекта) |
| `dependencies.require_auth` (заглушка) vs JWT | Два пути: MVP/бот и новые защищённые маршруты — зафиксировано как отклонение от «идеала» skill |

---

## Что ещё нужно проверить (рекомендуемый backlog)

**Ручное / интеграционное**

- [ ] Полный цикл **POST /v1/auth/login** → cookie → **GET /v1/auth/me** в браузере или клиенте с сохранением cookie; кириллица в `name` в UTF-8 (консоль Windows может искажать вывод — смотреть Swagger или файл).
- [ ] Выборочные вызовы под **роль teacher**: `GET /v1/teacher/schedule`, `GET /v1/students`, `PUT /v1/settings` после логина.
- [ ] **Роль student**: создать ученика с `password_hash` в БД или отдельный seed — проверить `GET /v1/student/schedule` (сейчас в тестах покрыт в основном teacher-flow).
- [ ] **E2E с ботом:** `make run` + backend с тем же `DATABASE_URL`, сценарий из `smoke-integration` в Makefile.

**CI / качество**

- [ ] Подключить **`ty check backend/src`** (или согласовать отказ в ADR) и цель в Makefile.
- [ ] **`pip-audit`** / Dependabot по рекомендации modern-python (периодически).
- [ ] Прогон **`make check`** из корня (бот + backend), не только `backend-test`.

**Контракты**

- [ ] **`make openapi-export`** и diff `docs/openapi.json` при изменении API.
- [ ] Сверка реализации с **`docs/tech/api-contracts.md`** после стабилизации полей в OpenAPI.

**Безопасность (прод)**

- [ ] Cookie: `Secure=True` за HTTPS; уточнить `SameSite` для своего домена фронта.
- [ ] Ротация `SECRET_KEY` и политика паролей преподавателя вне dev-seed.
