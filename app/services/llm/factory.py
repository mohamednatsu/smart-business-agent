from app.config import settings
from app.services.llm.groq_provider import GroqProvider
from app.services.llm.interface import LLMProvider


def get_llm_provider() -> LLMProvider:
    """Return the configured LLM provider.

    Currently returns Groq. Extend this factory when adding
    other providers (OpenAI, local models, etc.).
    """

    if not settings.groq_api_key:
        raise RuntimeError(
            "SBA_GROQ_API_KEY is not configured. Set it in .env or the environment."
        )

    return GroqProvider()
