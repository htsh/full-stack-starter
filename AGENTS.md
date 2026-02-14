# AGENTS.md

Repository-specific guidance for coding agents working in `/Users/hitesh/Code/full-stack-ai-app`.

## Scope

- Applies to the whole repository unless a deeper `AGENTS.md` exists in a subdirectory.
- Follow this file for repo behavior and workflows. Follow system/developer instructions for global policy.

## Project Overview

- Monorepo with:
  - `backend`: FastAPI + Beanie (MongoDB) + fastapi-users auth + Stripe integration.
  - `frontend`: React 19 + TypeScript + Vite + Tailwind v4 + Zustand.
- Local dev ports:
  - Backend: `http://localhost:8000`
  - Frontend: `http://localhost:7777`
- Frontend calls backend through Vite proxy at `/api` (see `frontend/vite.config.ts`).

## High-Signal File Map

- Backend app entry: `backend/app/main.py`
- Backend settings: `backend/app/config.py`
- DB initialization: `backend/app/database.py`
- Auth backend/router/manager:
  - `backend/app/auth/backend.py`
  - `backend/app/auth/router.py`
  - `backend/app/auth/manager.py`
- API routes:
  - `backend/app/routes/users.py`
  - `backend/app/routes/payments.py`
  - `backend/app/routes/ai.py`
- Business logic:
  - `backend/app/services/credits.py`
  - `backend/app/services/stripe.py`
  - `backend/app/services/ai.py`
- Frontend router: `frontend/src/router.tsx`
- Frontend auth store: `frontend/src/stores/auth-store.ts`
- Frontend API client/interceptors: `frontend/src/lib/api.ts`

## Setup And Run

- Initial setup:
  - `cp .env.example .env`
  - `make install`
- Start both apps:
  - `make dev`
- Start individually:
  - `make backend`
  - `make frontend`
- Docker:
  - `make docker-up`
  - `make docker-down`

## Validation Commands

- Frontend lint:
  - `cd frontend && pnpm lint`
- Frontend production build:
  - `cd frontend && pnpm build`
- Backend currently has no dedicated lint/test config in repo.
  - For backend-only edits, at minimum ensure app starts:
  - `cd backend && uv run uvicorn app.main:app --reload --port 8000`

## Change Conventions

### Backend

- Keep route handlers lightweight; place business logic in `backend/app/services/*`.
- Use `current_active_user` dependency for authenticated endpoints.
- Keep user credits mutations centralized via:
  - `add_credits` and `deduct_credits` in `backend/app/services/credits.py`.
- If credit package definitions are changed in `backend/app/services/stripe.py`, keep frontend package cards in `frontend/src/pages/Pricing.tsx` aligned.
- When adding new routes, include the router in `backend/app/main.py`.

### Frontend

- Use `frontend/src/lib/api.ts` for HTTP calls so auth interceptors apply.
- Preserve `@` alias imports (`@/`) for `src`.
- Protected pages should remain guarded in `frontend/src/router.tsx` with `ProtectedRoute`.
- Keep auth state shape in `frontend/src/stores/auth-store.ts` compatible with backend `UserRead` schema.

## Env And Secrets

- Required env vars are documented in `.env.example`.
- Relevant groups:
  - MongoDB: `MONGODB_URL`, `MONGODB_DB_NAME`
  - JWT/Auth secrets: `JWT_SECRET`, `RESET_PASSWORD_SECRET`, `VERIFICATION_SECRET`
  - Stripe: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, success/cancel URLs
  - App/Frontend: `BACKEND_CORS_ORIGINS`, `INITIAL_FREE_CREDITS`, `VITE_API_URL`
- Never commit `.env` or real secrets.

## Things To Avoid

- Do not edit generated or dependency directories (`backend/.venv`, `frontend/node_modules`, `dist` outputs).
- Do not hardcode secrets in source.
- Do not bypass auth/credit checks in API endpoints unless explicitly requested.

## Pre-Completion Checklist For Agents

- Run the most relevant validation commands for changed areas.
- Confirm endpoint/path consistency when backend/frontend contracts change.
- Keep changes focused; avoid unrelated refactors.
- Summarize what was changed, what was validated, and what was not validated.
