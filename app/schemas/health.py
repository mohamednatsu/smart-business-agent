from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str = Field(
        description="The health status of the application.", example="healthy"
    )

    service: str = Field(
        description="The name of the service.", example="Smart Business Agent"
    )

    version: str = Field(description="The version of the application.", example="0.1.0")
