# Задача 04: API-контракт сценария диалога

## Цель

Зафиксировать черновик HTTP API для сценария «ученик задаёт вопрос ассистенту» согласно [docs/idea.md](../../../../../idea.md), согласовать поля с [docs/data-model.md](../../../../../data-model.md) (`User`, `Dialogue`, `Message`), без дублирования полного OpenAPI (он будет на `/docs` после этапа 3–6).

## Что меняется

- [docs/integrations.md](../../../../../integrations.md): раздел **Backend HTTP API** — метод, назначение, основные поля; ссылка на [docs/api-conventions.md](../../../../../api-conventions.md).
- После выполнения задачи 05 тот же раздел ссылается на единый формат ошибок.

## Эндпоинт

| Метод и путь | Назначение |
|--------------|------------|
| `POST /v1/dialogue/message` | Принять сообщение ученика, вернуть ответ ассистента; создать/продолжить диалог |

Префикс версии и ошибки — в [docs/api-conventions.md](../../../../../api-conventions.md).

## Request body (JSON)

| Поле | Тип | Обязательность | Описание |
|------|-----|----------------|----------|
| `telegram_id` | `integer` | да | Идентификатор Telegram для поиска `User` с `role=student` (MVP до полноценной auth) |
| `text` | `string` | да | Текст вопроса ученика; не пустая строка после trim |
| `dialogue_id` | `string` (UUID) | нет | Продолжить существующий `Dialogue`; если отсутствует — создать новый диалог |

## Response `200 OK` (JSON)

| Поле | Тип | Описание |
|------|-----|----------|
| `dialogue_id` | `string` (UUID) | Идентификатор диалога (`Dialogue.id`) |
| `message_id` | `string` (UUID) | Идентификатор сохранённого ответа ассистента (`Message.id`, `role=assistant`) |
| `text` | `string` | Текст ответа ассистента |
| `created_at` | `string` (ISO 8601 UTC) | Время создания ответного сообщения |

На стороне БД параллельно сохраняется пользовательское сообщение (`Message.role=user`); его `id` в ответ MVP-контракта не обязателен (при необходимости расширить в задаче 13).

## Связь с data-model

- `Dialogue`: `student_id` ← `User` по `telegram_id`; `channel` = `telegram` для бота, `web` для веб-клиента (заголовок или поле можно добавить на этапе реализации).
- `Message`: `dialogue_id`, `role` (`user` / `assistant`), `content`, `created_at`.

## Примеры

### Запрос

```json
{
  "telegram_id": 123456789,
  "text": "Как решить квадратное уравнение?"
}
```

### Успех

```json
{
  "dialogue_id": "550e8400-e29b-41d4-a716-446655440000",
  "message_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "text": "Квадратное уравнение — это ...",
  "created_at": "2026-03-29T10:00:00Z"
}
```

## Ошибки (HTTP и коды тела)

См. [docs/api-conventions.md](../../../../../api-conventions.md). Типовые случаи:

| HTTP | `error.code` (ориентир) | Причина |
|------|-------------------------|---------|
| 422 | `validation_error` | Пустой `text`, некорректный JSON, и т.п. |
| 404 | `user_not_found` | Нет `User` с таким `telegram_id` (или не student) |
| 404 | `dialogue_not_found` | Передан неизвестный `dialogue_id` |
| 503 | `llm_unavailable` | Таймаут/ошибка OpenRouter |
| 500 | `internal_error` | Неожиданная ошибка сервера |

## Definition of Done

- В `integrations.md` есть сводка эндпоинта и ссылка на конвенции.
- Контракт не противоречит `data-model.md` для `Dialogue` / `Message`.
