# ADR-005: Расположение артефактов DevOps (devops/)

| Поле | Значение |
|------|----------|
| Статус | Принято |
| Дата | 2026-04-27 |

## Контекст

Нужны образы для backend, бота и frontend плюс единый `docker-compose.yml`. Dockerfile в корне репозитория либо один общий файл усложняют навигацию и смешивают контексты сборки. Предстоят GitHub Actions с явным `context` и `dockerfile` для каждого образа.

## Рассмотренные варианты

1. **Только корневые файлы** `Dockerfile.backend`, `Dockerfile.bot`, `Dockerfile.frontend` — много файлов в корне, сложнее группировать связанные `.dockerignore`.
2. **Один мультистейдж Dockerfile** на все сервисы — неочевидные цели, тяжёлый общий контекст.
3. **Каталог `devops/<service>/`** — Dockerfile и `.dockerignore` рядом, корень репо остаётся чистым.

## Решение

Принят вариант **3**:

- База: `devops/`.
- Вложенность **по сервисам**: `devops/backend/`, `devops/bot/`, `devops/frontend/`.
- Сборка: `docker build -f devops/backend/Dockerfile .` (и аналогично для bot/frontend); в Compose — `build.context: .`, `build.dockerfile: devops/.../Dockerfile`.

Это согласуется с матрицей jobs в GHA (отдельный build на сервис с тем же `context` и путём к Dockerfile).

## Последствия

- Новый сервис → новый подкаталог в `devops/<name>/`.
- `.dockerignore` дублируется по сервисам (можно позже вынести общие исключения в документацию или скрипт).
- Документация и onboarding ссылаются на `devops/` и корневой `docker-compose.yml`.
