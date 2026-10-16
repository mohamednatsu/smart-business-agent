import pytest
from pydantic import ValidationError

from app.schemas.task import BusinessTask, TaskType


def test_valid_task_parses():
    task = BusinessTask.model_validate(
        {
            "task_type": "sales_summary",
            "tool_name": "get_sales_summary",
            "tool_arguments": {"period": "month"},
            "reasoning": "User asked about sales.",
        }
    )
    assert task.task_type == TaskType.SALES_SUMMARY
    assert task.tool_name == "get_sales_summary"


def test_invalid_task_type_rejected():
    with pytest.raises(ValidationError):
        BusinessTask.model_validate(
            {
                "task_type": "not_a_real_type",
                "tool_name": None,
            }
        )


def test_missing_required_field_rejected():
    with pytest.raises(ValidationError):
        BusinessTask.model_validate(
            {
                "tool_name": "get_sales_summary",
            }
        )


def test_unknown_task_allows_null_tool():
    task = BusinessTask.model_validate(
        {
            "task_type": "unknown",
            "tool_name": None,
            "tool_arguments": {},
        }
    )

    assert task.task_type == TaskType.UNKNOWN
    assert task.tool_name is None
