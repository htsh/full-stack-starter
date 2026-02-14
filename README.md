# Full-Stack AI App Starter

A production-ready monorepo skeleton for building AI-powered SaaS apps. Users sign up, buy credits via Stripe, and spend them on AI features.

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI, Python 3.13, uv |
| Auth | fastapi-users (email/password + OAuth-ready) |
| Database | MongoDB via Beanie ODM |
| Payments | Stripe (one-time checkout, credit packages) |
| Frontend | React 19, Vite 7, TypeScript |
| UI | ShadCN + Tailwind CSS v4 |
| State | Zustand |
| HTTP | Axios with auth interceptor |
| Routing | React Router v7 |

## Project Structure

```
backend/           FastAPI app
  app/
    auth/          JWT auth, user manager, route aggregation
    models/        Beanie document models (User, Payment)
    routes/        API endpoints (users, payments, ai)
    services/      Business logic (stripe, credits, ai)
    config.py      Pydantic Settings
    database.py    Beanie/MongoDB init
    main.py        App entrypoint

frontend/          React SPA
  src/
    components/ui/ ShadCN components
    hooks/         useAuth, useCredits
    stores/        Zustand auth store
    pages/         Landing, Login, Register, Dashboard, Pricing, AppPage
    lib/           Axios instance, utils
    router.tsx     Routes with protected wrapper

deploy/            Production configs (nginx, systemd)
```

## Quick Start

### Prerequisites

- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- Node.js 22+ and [pnpm](https://pnpm.io/)
- MongoDB (local or Docker)

### Setup

```bash
cp .env.example .env
# Fill in your secrets (JWT_SECRET, Stripe keys, etc.)

make install   # installs backend + frontend deps
make dev       # starts backend on :8000, frontend on :5173
```

## Daily Dev Workflow

```bash
# one-time setup
make install

# start local hot-reload loop (backend + frontend)
make dev

# fast confidence checks before commit
make check

# strict frontend linting (currently may fail until lint debt is fixed)
make lint
```

Use your existing always-on MongoDB by setting `MONGODB_URL` in `.env`.

### Docker

```bash
docker compose up --build
```

This starts MongoDB, the backend (with hot-reload), and the frontend dev server.

## How It Works

### Auth Flow
- `fastapi-users` handles registration, login, JWT issuance, and password reset
- On registration, users receive free credits via the `on_after_register` hook
- Frontend stores JWT in Zustand (persisted to localStorage) and attaches it via Axios interceptor

### Payment Flow
1. User selects a credit package on `/pricing`
2. Backend creates a Stripe Checkout session → redirects user to Stripe
3. On successful payment, Stripe webhook fires → backend adds credits to user
4. Payment recorded in `payments` collection for audit

### Credit Packages
| Package | Credits | Price |
|---------|---------|-------|
| Starter | 50 | $4.99 |
| Pro | 200 | $14.99 |
| Mega | 500 | $29.99 |

### AI Endpoints
`POST /ai/generate` deducts 1 credit per request. Replace the placeholder in `services/ai.py` with your actual AI API calls.

## Deployment

For a single Ubuntu box:

1. Build frontend: `cd frontend && pnpm build`
2. Copy `deploy/nginx.conf` to `/etc/nginx/sites-enabled/`
3. Copy `deploy/backend.service` to `/etc/systemd/system/`
4. `systemctl enable --now backend`

Nginx serves the built frontend and proxies `/api/*` to uvicorn. Backend is stateless (JWT), so scaling means adding boxes behind a load balancer.

## Makefile Targets

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies |
| `make dev` | Start backend + frontend for development with one supervisor |
| `make check` | Run green-by-default quick checks |
| `make check-backend` | Verify backend imports and app wiring |
| `make check-frontend` | Build frontend for production |
| `make lint` | Run strict frontend linting |
| `make backend` | Start backend only |
| `make frontend` | Start frontend only |
| `make docker-up` | Start all services via Docker Compose |
| `make docker-down` | Stop Docker services |

## License

MIT
