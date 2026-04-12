# Итерация 0 — Требования к UI и API-контракты: план

## Цель

Зафиксировать функциональные требования ко всем 5 экранам frontend и спроектировать API-контракты для их реализации. По итогам итерации:

- существует полный документ требований (`docs/spec/frontend-requirements.md`),
- `docs/tech/api-contracts.md` содержит раздел «API для frontend» со всеми необходимыми маршрутами.

Ни одной строки кода в этой итерации не пишется — только документация.

---

## Ценность

Итерация является **фундаментом** для последующих итераций: без согласованных требований и API-контрактов невозможно параллельно реализовывать backend (Итерация 1) и frontend (Итерация 2+). Ранняя фиксация контрактов предотвращает дорогостоящие переработки интерфейса и схемы данных.

---

## Состав задач

| № | Задача | Артефакт |
|---|--------|----------|
| 01 | Функциональные требования к экранам | `docs/spec/frontend-requirements.md` |
| 02 | API-контракты для frontend | раздел в `docs/tech/api-contracts.md` |

Задачи выполняются последовательно: требования к экранам (01) определяют, какие данные нужны, что позволяет точно спроектировать контракты (02).

---

## Затрагиваемые файлы

| Действие | Файл |
|----------|------|
| Создать | `docs/spec/frontend-requirements.md` |
| Обновить | `docs/tech/api-contracts.md` (добавить раздел «API для frontend») |
| Создать | `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/plan.md` |
| Создать | `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-01-ui-requirements/summary.md` |
| Создать | `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/plan.md` |
| Создать | `docs/tasks/impl/frontend/iteration-0-ui-contracts/tasks/task-02-api-contracts/summary.md` |
| Создать | `docs/tasks/impl/frontend/iteration-0-ui-contracts/summary.md` (после завершения) |

---

## Экраны и роли (ориентир для обеих задач)

| Экран | Доступен ролям | Маршрут |
|-------|---------------|---------|
| Форма входа | все (неаутентифицированные) | `/login` |
| Календарь Преподавателя | teacher | `/teacher/calendar` |
| Ученики | teacher | `/teacher/students`, `/teacher/students/{id}` |
| Настройки системы | teacher | `/teacher/settings` |
| Расписание Ученика | student | `/student/schedule` |

---

## Связанные документы

- [`docs/vision.md`](../../../../vision.md) — архитектура, роли, принципы тонкого клиента
- [`docs/data-model.md`](../../../../data-model.md) — текущая схема данных
- [`docs/tech/api-contracts.md`](../../../../tech/api-contracts.md) — существующие контракты (MVP)
- [`docs/tasks/tasklist-frontend.md`](../../../tasklist-frontend.md) — сводный список задач

---

## Критерии готовности итерации

- [x] `docs/spec/frontend-requirements.md` создан и охватывает все 5 экранов + общие компоненты
- [x] `docs/tech/api-contracts.md` дополнен разделом «API для frontend»; дублирования с MVP-разделом нет
- [x] Все контракты покрывают данные, необходимые для отрисовки каждого экрана
- [x] Требования согласованы с `docs/vision.md` (тонкий клиент, роли student/teacher, backend как единственная логика)
- [x] Результаты проверки API по `api-design-principles` зафиксированы в `docs/tech/api-contracts.md` (подраздел «Проверка по api-design-principles»)

**Итог:** см. [summary.md](summary.md) — полная фиксация результатов итерации (артефакты, решения, риски, следующие шаги).
