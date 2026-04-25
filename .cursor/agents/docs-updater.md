---
name: docs-updater
description: >
  Актуализирует docs/tech/api-contracts.md, docs/openapi.json (через make openapi-export) и
  при необходимости onboarding при изменениях публичного HTTP API (backend FastAPI, роуты, схемы).
---

# docs-updater

**Полная инструкция (шаги, триггеры, критерии, ограничения):** [docs/agents/docs-updater.md](../../docs/agents/docs-updater.md)

## Кратко

| Когда | Что сделать |
|-------|-------------|
| Изменились `backend/.../api/`, публичные схемы, `/health`, `/v1/...` | `make openapi-export` → обновить [api-contracts.md](../../docs/tech/api-contracts.md) |
| Поменялся путь/команда для новичка или env для smoke | Точечно [onboarding.md](../../docs/onboarding.md) |

**Не** дублировать весь OpenAPI в markdown — в деталях опираться на [openapi.json](../../docs/openapi.json) и [api-conventions.md](../../docs/api-conventions.md).
