.PHONY: install dev check check-backend check-frontend lint backend frontend docker-up docker-down

install:
	cd backend && uv sync
	cd frontend && pnpm install

dev:
	sh scripts/dev.sh

check: check-backend check-frontend

check-backend:
	cd backend && uv run python -c "import app.main; print('backend import ok')"

check-frontend:
	cd frontend && pnpm build

lint:
	cd frontend && pnpm lint

backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && pnpm dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
