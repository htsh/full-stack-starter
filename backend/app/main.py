from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.auth.router import router as auth_router
from app.routes.users import router as users_router
from app.routes.payments import router as payments_router
from app.routes.ai import router as ai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Full-Stack AI App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(payments_router)
app.include_router(ai_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
