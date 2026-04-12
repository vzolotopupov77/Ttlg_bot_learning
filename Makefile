.PHONY: install run bot-test backend-install backend-run backend-db-up backend-db-migrate backend-db-reset backend-db-shell backend-db-logs backend-db-seed backend-db-test-create backend-test smoke-integration openapi-export lint format check

install:
	uv sync --all-packages

run:
	uv run python -m ttlg_bot

bot-test:
	uv run --all-packages pytest tests -v

# Ruff: бот + backend + Alembic (корневой pyproject workspace)
lint:
	uv run ruff check src backend/src backend/tests tests backend/alembic backend/scripts

format:
	uv run ruff format src backend/src backend/tests tests backend/alembic backend/scripts

check: lint backend-test bot-test

# Печатает чек-лист ручного smoke (бот + backend). См. README «End-to-end».
smoke-integration:
	@echo "Smoke (ручной): 1) .env: DATABASE_URL, OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN, BACKEND_URL"
	@echo "  2) make backend-db-up && make backend-db-migrate && make backend-db-seed"
	@echo "  3) POST /v1/users с вашим telegram_id (роль student)"
	@echo "  4) терминал 1: make backend-run"
	@echo "  5) терминал 2: make run"
	@echo "  6) Telegram: /start и сообщение с вопросом"

backend-install:
	uv sync --all-packages

backend-run:
	uv run --package ttlg-backend uvicorn ttlg_backend.main:app --reload --host 127.0.0.1 --port 8000

backend-db-up:
	docker compose up -d db

backend-db-migrate:
	uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

backend-db-reset:
	docker compose down -v
	docker compose up -d --wait db
	uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

backend-db-shell:
	docker compose exec db psql -U ttlg -d ttlg

backend-db-logs:
	docker compose logs -f db

backend-db-seed:
	uv run --package ttlg-backend python backend/scripts/seed.py

backend-db-test-create:
	-docker compose exec db psql -U ttlg -c "CREATE DATABASE ttlg_test;"

backend-test:
	uv run --package ttlg-backend pytest backend/tests -v

# Выгрузить OpenAPI JSON в docs/openapi.json (без запуска сервера)
openapi-export:
	uv run --package ttlg-backend python -c "import json, os, pathlib; os.environ.setdefault('SECRET_KEY','dev-openapi-export-only'); os.environ.setdefault('ACCESS_TOKEN_EXPIRE_MINUTES','60'); from ttlg_backend.main import app; pathlib.Path('docs/openapi.json').write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False), encoding='utf-8')"
