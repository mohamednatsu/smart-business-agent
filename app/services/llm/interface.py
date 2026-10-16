from abc import ABC, abstractmethod

from app.schemas.task import BusinessTask


class LLMProvider(ABC):
    """Abstract interface for LLM providers.

    Any provider (Groq, OpenAI, local model) must implement this
    interface so the rest of the application remains provider-agnostic.
    """

    @abstractmethod
    async def generate_task(self, user_request: str) -> BusinessTask:
        """Convert a natural-language request into a validated BusinessTask.

        Raises:
            LLMProviderError: If the provider fails or returns invalid output.
        """


class LLMProviderError(Exception):
    """Raised when an LLM provider fails after retries."""

    def __init__(self, message: str | None, original_error: Exception | None = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)
