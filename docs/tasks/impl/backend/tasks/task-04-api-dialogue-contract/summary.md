# Задача 04: API-контракт сценария диалога — summary

## Сделано

- Описан контракт `POST /v1/dialogue/message`: поля запроса (`telegram_id`, `text`, опционально `dialogue_id`), ответ `200` (`dialogue_id`, `message_id`, `text`, `created_at`).
- Сопоставление с [docs/data-model.md](../../../../../data-model.md): `Dialogue`, `Message`, поиск `User` по `telegram_id`.
- В [docs/integrations.md](../../../../../integrations.md) добавлен раздел **Backend HTTP API** со сводной таблицей и ссылкой на детали и конвенции.
- Создан канонический файл [docs/tech/api-contracts.md](../../../../../tech/api-contracts.md): таблицы полей, примеры JSON, заголовки, таблица ошибок, связь с data-model.

## Отклонения / решения

- `message_id` в ответе относится к сообщению ассистента; ID пользовательского сообщения в MVP-ответ не включён (расширение возможно в задаче 13).
- `dialogue_not_found (404)` возвращается и для несуществующего, и для чужого `dialogue_id` — намеренно, чтобы не раскрывать чужие идентификаторы.

## Проверка (api-design-principles)

- Выполнена проверка по skill `api-design-principles`: версия в URL, семантика `POST`, единый формат ошибок — соответствует принципам.
- Добавлены заметки по дизайну в `api-contracts.md`: URL-иерархия (future note), идемпотентность, rate limiting.
- Уязвимость `422`: выявлен стык FastAPI/Pydantic; устранено в задаче 05 (нормализация через `exception_handler`).
