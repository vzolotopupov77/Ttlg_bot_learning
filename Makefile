.PHONY: install run backend-install backend-run backend-db-up backend-db-migrate backend-test

install:
	uv sync --all-packages

run:
	uv run python -m ttlg_bot

backend-install:
	uv sync --all-packages

backend-run:
	uv run --package ttlg-backend uvicorn ttlg_backend.main:app --reload --host 127.0.0.1 --port 8000

backend-db-up:
	docker compose up -d db

backend-db-migrate:
	uv run --package ttlg-backend alembic -c backend/alembic.ini upgrade head

backend-test:
	uv run --package ttlg-backend --extra dev pytest backend/tests -v
