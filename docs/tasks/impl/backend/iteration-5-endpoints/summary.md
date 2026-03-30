# Итерация 5 (Backend): эндпоинты и серверная логика — summary

**Статус:** завершена

## Результат

- ORM + Alembic (`0001_initial_schema`), цель `make backend-db-migrate`.
- CRUD под `/v1`: users, lessons, assignments; прогресс — агрегирование.
- Модули `llm/` (OpenRouter-compatible), `services/dialogue_service.py`.
- Диалог: полная реализация контракта; stub и `assistant_reply` удалены.
- `make backend-test`: **16 passed** (включая CRUD smoke, LLM mock HTTP, 503 диалога).

## Ручная проверка без PostgreSQL (SQLite-файл + реальный LLM)

Позволяет проверить полный сценарий диалога без Docker.

**1. Переменные окружения** (выставить в `.env` или терминале):

```env
TTLG_ALLOW_SQLITE_TEST=1
DATABASE_URL=sqlite+aiosqlite:///./local_test.db
OPENROUTER_API_KEY=<ваш ключ>
LLM_MODEL=openai/gpt-4o-mini
```

**2. Запустить backend** — при старте `ensure_sqlite_schema` создаёт таблицы:

```bash
make backend-run
```

**3. Создать ученика** (`POST /v1/users` → **201**):

```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/v1/users `
  -ContentType "application/json" `
  -Body '{"name":"Тест","role":"student","telegram_id":123}'
```

**4. Отправить вопрос** (`POST /v1/dialogue/message` → **200** с реальным ответом LLM):

```powershell
Invoke-RestMethod -Method POST http://127.0.0.1:8000/v1/dialogue/message `
  -ContentType "application/json" `
  -Body '{"telegram_id":123,"text":"Как решить квадратное уравнение?"}'
```

Файл `local_test.db` можно открыть SQLite-клиентом и проверить таблицы `dialogues` / `messages`.

---

## Результаты ручной проверки (2026-03-30)

Проверка выполнена с SQLite-файлом и реальным LLM (OpenRouter, модель `openai/gpt-4o-mini`).

| Шаг | Результат |
|-----|-----------|
| `/health` | `{"status": "ok"}` |
| `POST /v1/users` | 201 Created, UUID возвращён |
| `POST /v1/dialogue/message` (новый диалог) | 200, реальный ответ LLM, `dialogue_id` = UUID |
| Продолжение диалога (`dialogue_id` тот же) | 200, тот же `dialogue_id` |

**Замечания:**
- Модель в `.env` обновлена с `stepfun/step-3.5-flash:free` → `openai/gpt-4o-mini` (бесплатные модели упирались в rate limit).
- Связь Bot → Backend ещё не реализована (задачи 17–18, этап 7).

## Отклонения

- UUID PK для всех сущностей — зафиксировано в summary задачи 10.
- Тесты по умолчанию используют SQLite in-memory при явном флаге окружения в фикстурах (не для продакшена).

## Задачи

| № | Summary |
|---|---------|
| 10 | [task-10-orm-migrations/summary.md](../tasks/task-10-orm-migrations/summary.md) |
| 11 | [task-11-crud-api/summary.md](../tasks/task-11-crud-api/summary.md) |
| 12 | [task-12-llm/summary.md](../tasks/task-12-llm/summary.md) |
| 13 | [task-13-dialogue-endpoint/summary.md](../tasks/task-13-dialogue-endpoint/summary.md) |
