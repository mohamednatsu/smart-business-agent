from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.llm.groq_provider import GroqProvider
from app.services.llm.interface import LLMProviderError


@pytest.fixture
def provider():
    return GroqProvider(api_key="test-key")


def _mock_completion(content: str):
    """Build a fake Groq completion response object."""

    choice = MagicMock()
    choice.message.content = content
    completion = MagicMock()
    completion.choices = [choice]

    return completion


@pytest.mark.asyncio
async def test_valid_json_produces_task(provider):
    valid_json = """
    {
      "task_type": "overdue_invoices",
      "tool_name": "list_overdue_invoices",
      "tool_arguments": {"min_days_overdue": 30},
      "reasoning": "User asked about overdue invoices."
    }
    """
    with patch.object(
        provider.client.chat.completions,
        "create",
        new=AsyncMock(return_value=_mock_completion(valid_json)),
    ):
        task = await provider.generate_task("Show me overdue invoices over 30 days")

    assert task.task_type.value == "overdue_invoices"
    assert task.tool_arguments == {"min_days_overdue": 30}


@pytest.mark.asyncio
async def test_malformed_json_raises_safe_error(provider):
    with (
        patch.object(
            provider.client.chat.completions,
            "create",
            new=AsyncMock(return_value=_mock_completion("not json at all")),
        ),
        pytest.raises(LLMProviderError) as exc_info,
    ):
        await provider.generate_task("Show me sales")

    assert "invalid JSON" in str(exc_info.value)


@pytest.mark.asyncio
async def test_schema_violation_raises_safe_error(provider):
    bad_schema = '{"task_type": "not_real", "tool_name": "get_sales_summary"}'
    with (
        patch.object(
            provider.client.chat.completions,
            "create",
            new=AsyncMock(return_value=_mock_completion(bad_schema)),
        ),
        pytest.raises(LLMProviderError) as exc_info,
    ):
        await provider.generate_task("Show me sales")

    assert "schema validation" in str(exc_info.value)


@pytest.mark.asyncio
async def test_api_failure_wrapped_as_provider_error(provider):
    with (
        patch.object(
            provider.client.chat.completions,
            "create",
            new=AsyncMock(side_effect=RuntimeError("network down")),
        ),
        pytest.raises(LLMProviderError) as exc_info,
    ):
        await provider.generate_task("Show me sales")

    assert "provider request failed" in str(exc_info.value)
