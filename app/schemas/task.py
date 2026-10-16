# app/schemas/task.py
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TaskType(StrEnum):
    """Enumeration of supported business task types."""

    SALES_SUMMARY = "sales_summary"
    OVERDUE_INVOICES = "overdue_invoices"
    POLICY_QUESTION = "policy_question"
    UNKNOWN = "unknown"


class BusinessTask(BaseModel):
    """Structured representation of a user's business request."""

    model_config = ConfigDict(
        use_enum_values=False,  # keep enum members, serialize to their value
        extra="ignore",  # tolerate extra fields from the LLM
        str_strip_whitespace=True,
    )

    task_type: TaskType = Field(description="The category of business request")
    tool_name: str | None = Field(default=None)
    tool_arguments: dict[str, Any] = Field(default_factory=dict)
    reasoning: str = Field(default="")


class LLMResponse(BaseModel):
    """Raw response wrapper from the LLM provider."""

    content: str
    model: str
    finish_reason: str | None = None
