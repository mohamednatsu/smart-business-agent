# app/api/tasks.py
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.schemas.task import BusinessTask
from app.services.llm.factory import get_llm_provider
from app.services.llm.interface import LLMProvider, LLMProviderError

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskRequest(BaseModel):
    request: str = Field(
        min_length=3,
        max_length=2000,
        description="Natural-language business request",
    )


class TaskResponse(BaseModel):
    task: BusinessTask
    source: str = Field(default="llm")


@router.post("", response_model=TaskResponse)
async def classify_task(
    payload: TaskRequest,
    provider: Annotated[LLMProvider, Depends(get_llm_provider)],
) -> TaskResponse:
    """Convert a natural-language request into a validated BusinessTask."""
    try:
        # ⬇⬇⬇ THIS AWAIT IS CRITICAL ⬇⬇⬇
        task = await provider.generate_task(payload.request)
    except LLMProviderError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM provider error: {e.message}",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        ) from e

    return TaskResponse(task=task, source="llm")
