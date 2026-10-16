from fastapi import FastAPI

from app.api.tasks import router as tasks_router
from app.config import settings
from app.schemas.health import HealthResponse

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description=(
        "Smart Business Agent — an evolving portfolio project for the "
        "20-Day Agentic AI Engineer Challenge."
    ),
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health_check() -> HealthResponse:
    """Health check endpoint to verify the application's status."""
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


app.include_router(tasks_router)
