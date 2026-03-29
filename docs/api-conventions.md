# Конвенции HTTP API (backend)

Документ задаёт единые правила для публичного API ядра. Полная машиночитаемая схема — в OpenAPI на `GET /docs` после реализации (задачи 06–14).

---

## Версионирование пути

- Все публичные маршруты располагаются под префиксом **`/v1`**.
- Пример: `POST /v1/dialogue/message`.

---

## Формат ошибки

Тело ответа при ошибке (кроме случаев, когда прокси/infra возвращает non-JSON):

```json
{
  "error": {
    "code": "user_not_found",
    "message": "User with given telegram_id was not found"
  }
}
```

Правила:

- **`code`** — стабильная строка для клиентов и логов (snake_case).
- **`message`** — кратко, без секретов, без полного текста исключений и без чувствительных данных.
- Детали для отладки — только в серверных логах (осторожно с PII).

---

## HTTP-статусы

| Статус | Когда используется |
|--------|---------------------|
| `200` | Успешное чтение или обработка с телом ответа (в т.ч. «сообщение принято, ответ ассистента в теле»). |
| `201` | Ресурс создан (если эндпоинт явно про create и возвращает созданную сущность). |
| `400` | Некорректные параметры запроса в бизнес-смысле (редко; часть кейсов перекрывает `422`). |
| `404` | Сущность не найдена (`user_not_found`, `dialogue_not_found` и т.д.). |
| `422` | Ошибка валидации тела/параметров. FastAPI/Pydantic по умолчанию возвращает `{"detail": [...]}` — в реализации **нормализовать** через `exception_handler` в единый формат `{"error": {...}}` (см. ниже). |
| `500` | Внутренняя ошибка (`internal_error` или без утечки деталей наружу). |
| `503` | Временная недоступность зависимости (например LLM: `llm_unavailable`). |

Клиентам: ориентироваться на **HTTP-статус**; `error.code` — для уточнения ветвления UI/логики.

### Нормализация `422` в реализации

FastAPI вызывает `RequestValidationError` с телом `{"detail": [...]}`. Добавить в `main.py` (или фабрику приложения) обработчик:

```python
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Request validation failed"}},
    )
```

Детали нарушений — в лог, не в ответ.

---

## Заголовки

| Заголовок | Назначение |
|-----------|------------|
| `X-User-Role` | Опционально: `student` \| `teacher` — задел под ролевую модель до полноценной auth (JWT, session). На этапе диалога бота может не передаваться. |

---

## Связанные документы

- Контракты эндпоинтов: [tech/api-contracts.md](tech/api-contracts.md).
- Сводка для интеграций: [docs/integrations.md](integrations.md) → раздел **Backend HTTP API**.
- План задачи (этап планирования): [task-04 plan](tasks/impl/backend/tasks/task-04-api-dialogue-contract/plan.md).
