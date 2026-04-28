# Дорожная карта

**Актуализация:** 2026-04-27 — добавлена отметка о ручном смоуке локального полного стека в Docker; продуктовые итерации 1–6 без изменений по сравнению с 2026-04-22.

## Организация работ

`plan.md` задаёт **продуктовые** итерации (что должно появиться в системе). Детальная декомпозиция — в **tasklist** по областям:

| Область | Основной tasklist | Примечание |
|---------|-------------------|------------|
| DevOps (Docker, GHCR) | [tasklist-devops.md](tasks/tasklist-devops.md) | Итерация 1: локальный полный стек в Compose — **выполнена**, ручной продуктовый смоук **2026-04-27** ([how-to-docker.md](how-to-docker.md#ручная-проверка-зафиксировано)). Итерация 2 (GHCR/GHA): по [tasklist-devops.md](tasks/tasklist-devops.md) — 📋. |
| Бот | [tasklist-bot-iteration-1-basic-bot.md](tasks/tasklist-bot-iteration-1-basic-bot.md), [tasklist-bot-iteration-3-personalized-dialog.md](tasks/tasklist-bot-iteration-3-personalized-dialog.md) | Итерации плана 1 и 3 |
| Backend (ядро) | [tasklist-backend.md](tasks/tasklist-backend.md), [tasklist-backend-iteration-2-core.md](tasks/tasklist-backend-iteration-2-core.md) | Итерация плана 2 + ежедневные задачи |
| Frontend (веб) | **[tasklist-frontend.md](tasks/tasklist-frontend.md)** | Итерации **0–8** (от требований до тестов); единый файл |
| Черновик расширений | [tasklist-backend-iteration-6-progress.md](tasks/tasklist-backend-iteration-6-progress.md) | Не синхронизирован с фактом; см. примечание в файле |
| Заглушка (ит. 4 плана) | [tasklist-backend-iteration-4-schedule-hw.md](tasks/tasklist-backend-iteration-4-schedule-hw.md) | MVP закрыт в API; файл — краткая ссылка на контракты |

## Ключевые особенности плана

**API-first.** Backend — ядро; бот и веб — тонкие клиенты. Сначала контракты и данные, затем клиенты.

**Инкрементальная ценность.** Каждая итерация даёт проверяемый результат.

**Параллелизация по областям.** Бот и backend могли развиваться параллельно; веб опирается на стабильный API (`docs/tech/api-contracts.md`).

## Легенда статусов

- 📋 Planned — запланировано, не начато или не доведено
- 🚧 In Progress — в работе / частично
- ✅ Done — по текущему объёму MVP выполнено

---

## Обзор итераций

| № | Название | Цель | Статус | Детализация |
|---|----------|------|--------|-------------|
| 1 | Базовый бот с LLM | Рабочий бот с диалогом через LLM | ✅ Done | [tasklist-bot-iteration-1-basic-bot.md](tasks/tasklist-bot-iteration-1-basic-bot.md) |
| 2 | Backend Core | FastAPI + PostgreSQL + доменная модель | ✅ Done | [tasklist-backend-iteration-2-core.md](tasks/tasklist-backend-iteration-2-core.md), [tasklist-backend.md](tasks/tasklist-backend.md) |
| 3 | Персонализированный диалог | Бот как тонкий клиент; контекст из БД в LLM | ✅ Done | [tasklist-bot-iteration-3-personalized-dialog.md](tasks/tasklist-bot-iteration-3-personalized-dialog.md) |
| 4 | Расписание и домашние задания | Занятия, ДЗ, напоминания через backend | ✅ Done (MVP) | Реализовано в API под веб и бота: CRUD занятий, флаги, ДЗ, эндпоинты преподавателя (расписание, напоминания, переносы). См. [tasklist-backend-iteration-4-schedule-hw.md](tasks/tasklist-backend-iteration-4-schedule-hw.md) (якорь + ссылки на контракты). |
| 5 | Веб-интерфейс | Фронтенд для ученика и преподавателя | ✅ Done | **[tasklist-frontend.md](tasks/tasklist-frontend.md)** (итерации 0–8). |
| 6 | Прогресс и аналитика | Агрегации, отчёты, обогащение контекста LLM | 🚧 Частично | Есть `GET /v1/users/{user_id}/progress`, `GET /v1/students/{id}/stats`, отображение на детальной странице ученика. Нет полного слоя «отчёты/тренды для всех» и доработок из [tasklist-backend-iteration-6-progress.md](tasks/tasklist-backend-iteration-6-progress.md). |

---

## Итерации (описание)

### Итерация 1: Базовый бот с LLM

**Статус:** ✅ Done.

**Цель:** минимальный бот: сообщения ученика → ответ через OpenRouter.

**Критерии завершения (DoD):**

- Запуск бота без ошибок; `/start` и текст обрабатываются
- Ответ LLM доходит в Telegram
- Конфиг через `pydantic-settings` + `.env`; `.env.example` в репо

**Tasklist:** [tasklist-bot-iteration-1-basic-bot.md](tasks/tasklist-bot-iteration-1-basic-bot.md)

**Артефакты:** `src/` (бот), корневой `pyproject.toml`, `Makefile`, `.env.example`

---

### Итерация 2: Backend Core

**Статус:** ✅ Done.

**Цель:** FastAPI + PostgreSQL, доменные сущности, базовые API.

**Критерии завершения (DoD):**

- Сервис запускается (`make backend-run` и тестовый раннер)
- Схема и миграции; CRUD и smoke-тесты
- `DATABASE_URL` и секреты из `.env`

**Tasklist:** [tasklist-backend-iteration-2-core.md](tasks/tasklist-backend-iteration-2-core.md), далее [tasklist-backend.md](tasks/tasklist-backend.md)

**Артефакты:** `backend/`, Alembic, `docs/data-model.md`, ADR по стеку

---

### Итерация 3: Персонализированный диалог

**Статус:** ✅ Done.

**Цель:** бот вызывает backend API; контекст занятий и ДЗ в промпте; история в `Dialogue` / `Message`.

**Tasklist:** [tasklist-bot-iteration-3-personalized-dialog.md](tasks/tasklist-bot-iteration-3-personalized-dialog.md)

---

### Итерация 4: Расписание и домашние задания

**Статус:** ✅ Done (MVP по продукту).

**Цель (изначально):** цикл занятий и ДЗ, напоминания, ответы бота о расписании.

**Факт:** эндпоинты и модель закрывают сценарии веб-MVP и сопутствующую логику (см. [api-contracts.md](tech/api-contracts.md)): уроки с флагами, ДЗ, панели преподавателя, переносы. Краткая заметка и ссылки: [tasklist-backend-iteration-4-schedule-hw.md](tasks/tasklist-backend-iteration-4-schedule-hw.md).

**Оставшиеся улучшения** (вне закрытого MVP): узкоспециализированные сценарии бота («что задано?» как отдельные хендлеры), политика статусов ДЗ, фоновые напоминания — по необходимости заводятся новыми задачами.

---

### Итерация 5: Веб-интерфейс

**Статус:** ✅ Done.

**Цель:** единый веб-клиент для `student` и `teacher`.

**Факт:** реализовано в **[tasklist-frontend.md](tasks/tasklist-frontend.md)** — итерации 0–8 (требования, API для фронта, каркас, календарь, ученики, настройки, расписание ученика, ревью качества, тесты). Спецификация экранов: [spec/frontend-requirements.md](spec/frontend-requirements.md).

**Артефакты:** `frontend/`, Vitest + MSW, документация в `docs/tasks/impl/frontend/`.

---

### Итерация 6: Прогресс и аналитика

**Статус:** 🚧 Частично.

**Цель:** агрегации за период, отчёты, обогащение LLM.

**Факт:** частично — прогресс/статы по ученику в API и на UI детальной карточки; общие отчёты, тренды, расширенный LLM-контекст — **не закрыты**. Ориентир по будущим задачам: [tasklist-backend-iteration-6-progress.md](tasks/tasklist-backend-iteration-6-progress.md) (требует пересмотра под факт).

---

## Следующие шаги (вне закрытого MVP)

1. Завершить или переписать **итерацию 6** в tasklist'ах под реальные приоритеты (отчёты, бот, LLM).
2. Новые продуктовые цели — **новая строка** в таблице обзора и новый tasklist/итерация по правилам в [`.cursor/rules/workflow.mdc`](../.cursor/rules/workflow.mdc).
