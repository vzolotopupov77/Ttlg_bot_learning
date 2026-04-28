.PHONY: install run bot-test backend-install backend-run backend-db-up backend-db-migrate backend-db-reset backend-db-shell backend-db-logs backend-db-seed backend-db-test-create backend-test smoke-integration openapi-export lint format check frontend-dev frontend-build frontend-lint frontend-test stack-build stack-up stack-down stack-ps stack-logs stack-health stack-migrate help

# Полный стек в Docker (см. docs/how-to-docker.md)
stack-build: ## Собрать образы (docker compose build)
	docker compose build

stack-up: ## Поднять db + backend + bot + frontend
	docker compose up -d --build

stack-down: ## Остановить и убрать контейнеры стека
	docker compose down

stack-ps: ## Статус сервисов compose
	docker compose ps

stack-logs: ## Логи всех сервисов (-f)
	docker compose logs -f

stack-logs-%: ## Логи одного сервиса: make stack-logs-backend
	docker compose logs -f $*

stack-health: ## Стек: HTTP backend /health + frontend :3000; docker compose ps (db, backend, bot, frontend)
	@python scripts/stack_health.py

stack-migrate: ## Alembic upgrade в одноразовом контейнере backend (сеть к db)
	docker compose run --rm backend alembic -c backend/alembic.ini upgrade head

help: ## Список целей Make (кратко); без grep — работает из PowerShell (нужен python в PATH)
	@python scripts/make_help.py

install: ## Зависимости workspace (uv sync --all-packages)
	uv sync --all-packages

run: ## Запуск Telegram-бота (long polling)
	uv run python -m ttlg_bot

bot-test: ## pytest интеграции бота (tests/)
	uv run --all-packages pytest tests -v

# Ruff: бот + backend + Alembic (корневой pyproject workspace)
lint: ## Ruff check (бот, backend, тесты, Alembic)
	uv run ruff check src backend/src backend/tests tests backend/alembic backend/scripts

format: ## Ruff format
	uv run ruff format src backend/src backend/tests tests backend/alembic backend/scripts

check: lint backend-test bot-test frontend-lint ## lint + backend-test + bot-test + frontend-lint

frontend-dev: ## Next.js dev-сервер
	pnpm --filter frontend dev

frontend-build: ## Next.js production build
	pnpm --filter frontend build

frontend-lint: ## ESLint frontend
	pnpm --filter frontend lint

frontend-test: ## Vitest frontend
	pnpm --filter frontend test

# Печатает чек-лист ручного smoke (бот + backend). См. README «End-to-end».
smoke-integration: ## Подсказка по ручному E2E (бот + backend)
	@echo "Smoke (ручной): 1) .env: DATABASE_URL, OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN, BACKEND_URL"
	@echo "  2) make backend-db-up && make backend-db-migrate && make backend-db-seed"
	@echo "  3) POST /v1/users с вашим telegram_id (роль student)"
	@echo "  4) терминал 1: make backend-run"
	@echo "  5) терминал 2: make run"
	@echo "  6) Telegram: /start и сообщение с вопросом"

backend-install: ## То же, что install (uv workspace)
	uv sync --all-packages

backend-run: ## FastAPI + reload на 127.0.0.1:8000
	uv run --package ttlg-backend uvicorn ttlg_backend.main:app --reload --host 127.0.0.1 --port 8000

backend-db-up: ## Только PostgreSQL в Docker (сервис db)
	docker compose up -d db

backend-db-migrate: ## Alembic upgrade head (с хоста, нужен DATABASE_URL на localhost)
	uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

backend-db-reset: ## down -v, поднять db, снова migrate
	docker compose down -v
	docker compose up -d --wait db
	uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

backend-db-shell: ## psql в контейнере db
	docker compose exec db psql -U ttlg -d ttlg

backend-db-logs: ## Логи сервиса db
	docker compose logs -f db

backend-db-seed: ## Тестовые данные (seed.py)
	uv run --package ttlg-backend python backend/scripts/seed.py

backend-db-test-create: ## CREATE DATABASE ttlg_test (игнор ошибки, если есть)
	-docker compose exec db psql -U ttlg -c "CREATE DATABASE ttlg_test;"

backend-test: ## pytest backend/tests
	uv run --package ttlg-backend pytest backend/tests -v

# Выгрузить OpenAPI JSON в docs/openapi.json (без запуска сервера)
openapi-export: ## Записать docs/openapi.json из FastAPI app
	uv run --package ttlg-backend python -c "import json, os, pathlib; os.environ.setdefault('SECRET_KEY','dev-openapi-export-only'); os.environ.setdefault('ACCESS_TOKEN_EXPIRE_MINUTES','60'); from ttlg_backend.main import app; pathlib.Path('docs/openapi.json').write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False), encoding='utf-8')"
