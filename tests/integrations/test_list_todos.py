import pytest
from uuid import UUID
from pytest_steps import test_steps
from httpx import AsyncClient
from src.constants import TodoStatusEnum, TodoPriorityEnum

from tests.generator import generate_todo_create_data
from tests.tools.response_helpers import assert_todo_list_response_structure
from tests.utils import extract_todo_id_from_response


async def _create_test_todos(client: AsyncClient, count: int):
    """Helper to create multiple test todos."""
    todo_ids = []
    for i in range(count):
        todo_data = generate_todo_create_data(title=f"Test Todo {i+1}")
        response = await client.post("/api/v1/todos", json=todo_data)
        assert response.status_code == 201
        todo_ids.append(extract_todo_id_from_response(response.json()))
    return todo_ids


@pytest.mark.asyncio
@test_steps(
    "create_test_todos",
    "list_all_todos",
    "verify_response_structure",
    "verify_all_todos_returned",
)
async def test_list_all_todos(test_client: AsyncClient):
    """Test listing all todos."""
    created_ids = await _create_test_todos(test_client, 3)

    yield created_ids

    response = await test_client.get("/api/v1/todos")

    yield response

    assert response.status_code == 200

    yield response

    response_data = response.json()
    assert_todo_list_response_structure(response_data)

    yield response_data

    returned_ids = [UUID(todo["id"]) for todo in response_data["todos"]]
    assert len([tid for tid in created_ids if tid in returned_ids]) >= 3


@pytest.mark.asyncio
@test_steps(
    "create_todos_with_different_statuses",
    "filter_by_status",
    "verify_filtered_results",
)
async def test_list_todos_filtered_by_status(test_client: AsyncClient):
    """Test listing todos filtered by status."""
    from tests.generator import generate_todo_update_data

    todo_data = generate_todo_create_data(title="Test Todo for Status Filter")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())

    update_data = generate_todo_update_data(status=TodoStatusEnum.IN_PROGRESS)
    await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)

    yield todo_id

    response = await test_client.get("/api/v1/todos?status=in_progress")

    yield response

    assert response.status_code == 200

    yield response

    response_data = response.json()
    assert_todo_list_response_structure(response_data)
    assert all(todo["status"] == "in_progress" for todo in response_data["todos"])


@pytest.mark.asyncio
@test_steps(
    "create_todos_with_different_priorities",
    "filter_by_priority",
    "verify_filtered_results",
)
async def test_list_todos_filtered_by_priority(test_client: AsyncClient):
    """Test listing todos filtered by priority."""
    todo_data = generate_todo_create_data(
        title="High Priority Todo", priority=TodoPriorityEnum.HIGH
    )
    await test_client.post("/api/v1/todos", json=todo_data)

    yield todo_data

    response = await test_client.get("/api/v1/todos?priority=high")

    yield response

    assert response.status_code == 200

    yield response

    response_data = response.json()
    assert_todo_list_response_structure(response_data)
    assert all(todo["priority"] == "high" for todo in response_data["todos"])


@pytest.mark.asyncio
@test_steps("create_multiple_todos", "apply_pagination", "verify_pagination_works")
async def test_list_todos_with_pagination(test_client: AsyncClient):
    """Test listing todos with pagination."""
    await _create_test_todos(test_client, 5)

    yield None

    response = await test_client.get("/api/v1/todos?limit=2&offset=0")

    yield response

    assert response.status_code == 200

    yield response

    response_data = response.json()
    assert_todo_list_response_structure(response_data)
    assert response_data["limit"] == 2
    assert response_data["offset"] == 0
    assert len(response_data["todos"]) <= 2


@pytest.mark.asyncio
@test_steps("apply_combined_filters", "verify_filtered_and_paginated_results")
async def test_list_todos_with_combined_filters(test_client: AsyncClient):
    """Test listing todos with combined filters."""
    from tests.generator import generate_todo_update_data

    todo_data = generate_todo_create_data(
        title="Filtered Todo", priority=TodoPriorityEnum.MEDIUM
    )
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())

    update_data = generate_todo_update_data(status=TodoStatusEnum.PENDING)
    await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)

    yield todo_id

    response = await test_client.get(
        "/api/v1/todos?status=pending&priority=medium&limit=10"
    )

    yield response

    assert response.status_code == 200
    response_data = response.json()
    assert_todo_list_response_structure(response_data)
    assert all(
        todo["status"] == "pending" and todo["priority"] == "medium"
        for todo in response_data["todos"]
    )
