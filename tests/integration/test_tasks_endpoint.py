# tests/integration/test_tasks_endpoint.py
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.task import BusinessTask, TaskType
from app.services.llm.factory import get_llm_provider


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_task() -> BusinessTask:
    return BusinessTask(
        task_type=TaskType.SALES_SUMMARY,
        tool_name="get_sales_summary",
        tool_arguments={"period": "month"},
        reasoning="User asked for monthly sales.",
    )


@pytest.fixture
def mock_provider(mock_task: BusinessTask) -> AsyncMock:
    """AsyncMock whose awaited generate_task returns a BusinessTask."""
    provider = AsyncMock()
    provider.generate_task.return_value = mock_task
    return provider


def test_classify_task_returns_validated_task(
    client: TestClient,
    mock_provider: AsyncMock,
):
    app.dependency_overrides[get_llm_provider] = lambda: mock_provider
    try:
        response = client.post(
            "/tasks",
            json={"request": "What were sales last month?"},
        )
    finally:
        app.dependency_overrides.clear()

    # Show the body when the test fails — invaluable for debugging
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["task"]["task_type"] == "sales_summary"
    assert data["task"]["tool_name"] == "get_sales_summary"
    assert data["task"]["tool_arguments"] == {"period": "month"}
    assert data["source"] == "llm"
