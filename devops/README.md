# devops

Каталог артефактов контейнеризации: по одному подкаталогу на сервис.

| Путь | Назначение |
|------|------------|
| `backend/` | Dockerfile и `.dockerignore` для FastAPI (`ttlg-backend`) |
| `bot/` | Dockerfile и `.dockerignore` для Telegram-бота (`ttlg-bot`) |
| `frontend/` | Dockerfile и `.dockerignore` для Next.js (`frontend`) |

Контекст сборки — **корень репозитория**; пути в `docker-compose.yml`: `dockerfile: devops/<service>/Dockerfile`, `context: .`.

**Важно:** при `context: .` Docker использует только **[`.dockerignore` в корне репозитория](../.dockerignore)**. Файлы `devops/*/.dockerignore` — справочные списки для сервиса; без корневого ignore в контекст попадут, например, `node_modules` и `.next` (сотни МБ / ГБ).

См. [ADR-005](../docs/adr/adr-005-devops-artifacts-layout.md).
