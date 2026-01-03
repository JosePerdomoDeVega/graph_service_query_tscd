from fastapi import FastAPI

from application.api_routers import health
from application.api_routers.jobs import router as queue_jobs_router
from application.api_routers.return_job_result import router as get_done_jobs_router
from services.logger.logger import get_logger
from domain.settings.settings import get_settings


def create_app() -> FastAPI:
    """
    Application factory.
    Creates and configures the FastAPI application.
    """
    settings = get_settings()
    logger = get_logger()

    app = FastAPI(
        title="Graph Service Query",
        description="Public API for asynchronous word graph queries",
        version="0.1.0"
    )

    app.include_router(health.router, tags=["health"])
    app.include_router(queue_jobs_router, tags=["jobs"])
    app.include_router(get_done_jobs_router, tags=["done_jobs"])

    logger.info("Graph Service Query application initialized")

    return app


app = create_app()
