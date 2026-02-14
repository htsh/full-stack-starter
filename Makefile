.PHONY: install dev backend frontend docker-up docker-down

install:
	cd backend && uv sync
	cd frontend && pnpm install

dev:
	$(MAKE) backend &
	$(MAKE) frontend &
	wait

backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && pnpm dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
