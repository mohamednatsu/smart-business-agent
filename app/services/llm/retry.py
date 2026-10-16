import logging
from collections.abc import Callable
from typing import Any, TypeVar

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.config import settings
from app.services.llm.interface import LLMProviderError

logger = logging.getLogger(__name__)

T = TypeVar("T")


def with_retry(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to retry a function call with exponential backoff."""

    @retry(
        retry=retry_if_exception_type((LLMProviderError, TimeoutError)),
        stop=stop_after_attempt(settings.llm_max_retries + 1),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except LLMProviderError as e:
            # Do not retry on schema validation errors — retrying won't help
            if "schema validation" in str(e) or "invalid JSON" in str(e):
                logger.warning("Non-retryable LLM error: %s", e)
                raise

            logger.info("Retrying LLM call after error: %s", e)
            raise

    return wrapper
