from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.redis.connection import redis_manager
from app.utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(debug=settings.debug)
    if settings.environment != "testing":
        await redis_manager.connect()
    yield
    await redis_manager.close()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
