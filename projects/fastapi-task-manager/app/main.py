"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.logging_config import logger
from app.routers import health, tasks


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Initialize database tables when the API starts."""
    if not settings.testing:
        init_db()
        logger.info("Application started")
    yield
    if not settings.testing:
        logger.info("Application stopped")


app = FastAPI(
    title=settings.app_name,
    description="A practical REST API for managing tasks with FastAPI and SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(health.router)
app.include_router(tasks.router)
