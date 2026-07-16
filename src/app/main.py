"""FastAPI application entrypoint: factory, lifespan, health route."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes_health import router as health_router
from .config import get_settings
from .logging import configure_logging, get_logger
from .persistence.db import dispose_engine
from .redis_client import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    settings = get_settings()
    get_logger("app").info(
        "app.startup",
        version=settings.app_version,
        embeddings_provider=settings.embeddings_provider,
        generation_provider=settings.generation_provider or "unset",
    )
    yield
    await dispose_engine()
    await close_redis()
    get_logger("app").info("app.shutdown")


def create_app() -> FastAPI:
    app = FastAPI(
        title="enterprise-rag",
        version=get_settings().app_version,
        summary="RAG knowledge assistant over internal documents (reference implementation).",
        lifespan=lifespan,
    )
    app.include_router(health_router)
    return app


app = create_app()
