import json
import logging

from groq import AsyncGroq
from pydantic import ValidationError

from app.config import settings
from app.schemas.task import BusinessTask
from app.services.llm.interface import LLMProvider, LLMProviderError
from app.services.llm.retry import with_retry

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a business task classifier for Smart Business Agent.
Your job is to convert natural-language business requests into a structured task.

Available task types:
- sales_summary: Questions about sales figures, revenue, or product performance.
- overdue_invoices: Questions about unpaid or overdue customer invoices.
- policy_question: Questions about company policies or procedures.
- unknown: Anything that does not fit the above categories.

Available tools (use only these exact names):
- get_sales_summary: Returns sales data. Arguments: {"period": "month|quarter|year"}
- list_overdue_invoices: Returns overdue invoices. Arguments: {"min_days_overdue": int}

Always respond with valid JSON matching the required schema.
If you are unsure, set task_type to "unknown" and tool_name to null.
"""


class GroqProvider(LLMProvider):
    """LLM provider implementation using Groq's API."""

    def __init__(self, api_key: str | None = None):
        key = api_key or settings.groq_api_key
        if not key:
            raise LLMProviderError("""LLM provider implementation using Groq's API.""")

        self.client = AsyncGroq(api_key=key)
        self.model = settings.llm_model

    @with_retry
    async def generate_task(self, user_request) -> BusinessTask:
        """Call Groq and parse the response into a BusinessTask."""

        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_request},
                ],
                response_format={
                    "type": "json_object",
                },
                temperature=0.1,
                max_tokens=settings.max_token,
                timeout=settings.llm_timeout_seconds,
            )

        except Exception as e:
            logger.error("Groq API Call failed: %s", e)
            raise LLMProviderError(
                f"LLM provider request failed: {e}", original_error=e
            ) from e

        raw_content = completion.choices[0].message.content or ""

        # Parse and validate - this is the safety boundary

        try:
            data = json.loads(raw_content)
        except json.JSONDecodeError as e:
            logger.warning("LLM returned invalid JSON: %s", raw_content[:200])

            raise LLMProviderError(
                f"LLM returned invalid JSON: {e}", original_error=e
            ) from e

        try:
            return BusinessTask.model_validate(data)

        except ValidationError as e:
            logger.warning("LLM output failed schema validation: %s", e)
            raise LLMProviderError(
                f"LLM output failed schema validation: {e}", original_error=e
            ) from e
