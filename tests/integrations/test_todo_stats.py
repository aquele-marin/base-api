import pytest
from pytest_steps import test_steps
from httpx import AsyncClient
from src.constants import TodoStatusEnum, TodoPriorityEnum

from tests.generator import generate_todo_create_data, generate_todo_update_data
from tests.tools.response_helpers import assert_todo_stats_response_structure
from tests.utils import extract_todo_id_from_response


async def _create_todos_with_statuses(client: AsyncClient):
    """Helper to create todos with different statuses."""
    todo1 = generate_todo_create_data(title="Pending Todo")
    todo2 = generate_todo_create_data(title="In Progress Todo")
    todo3 = generate_todo_create_data(title="Completed Todo 1")
    todo4 = generate_todo_create_data(title="Completed Todo 2")
    
    resp1 = await client.post("/api/v1/todos", json=todo1)
    resp2 = await client.post("/api/v1/todos", json=todo2)
    resp3 = await client.post("/api/v1/todos", json=todo3)
    resp4 = await client.post("/api/v1/todos", json=todo4)
    
    todo2_id = extract_todo_id_from_response(resp2.json())
    todo3_id = extract_todo_id_from_response(resp3.json())
    todo4_id = extract_todo_id_from_response(resp4.json())
    
    update2 = generate_todo_update_data(status=TodoStatusEnum.IN_PROGRESS)
    update3 = generate_todo_update_data(status=TodoStatusEnum.COMPLETED)
    update4 = generate_todo_update_data(status=TodoStatusEnum.COMPLETED)
    
    await client.put(f"/api/v1/todos/{todo2_id}", json=update2)
    await client.put(f"/api/v1/todos/{todo3_id}", json=update3)
    await client.put(f"/api/v1/todos/{todo4_id}", json=update4)


@pytest.mark.asyncio
@test_steps("get_stats_with_no_todos", "verify_empty_stats")
async def test_get_todo_stats_empty(test_client: AsyncClient):
    """Test getting stats when there are no todos."""
    response = await test_client.get("/api/v1/todos/stats")
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_stats_response_structure(response_data)
    assert response_data["total"] == 0
    assert response_data["pending"] == 0
    assert response_data["in_progress"] == 0
    assert response_data["completed"] == 0


@pytest.mark.asyncio
@test_steps("create_todos_with_different_statuses", "get_stats", "verify_correct_counts")
async def test_get_todo_stats_with_todos(test_client: AsyncClient):
    """Test getting stats with todos in different statuses."""
    await _create_todos_with_statuses(test_client)
    
    yield None
    
    response = await test_client.get("/api/v1/todos/stats")
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_stats_response_structure(response_data)
    assert response_data["total"] >= 4
    assert response_data["pending"] >= 1
    assert response_data["in_progress"] >= 1
    assert response_data["completed"] >= 2


@pytest.mark.asyncio
@test_steps("create_single_todo", "get_stats", "verify_counts")
async def test_get_todo_stats_single_todo(test_client: AsyncClient):
    """Test getting stats with a single todo."""
    todo_data = generate_todo_create_data(title="Single Todo Stats")
    await test_client.post("/api/v1/todos", json=todo_data)
    
    yield None
    
    response = await test_client.get("/api/v1/todos/stats")
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_stats_response_structure(response_data)
    assert response_data["total"] >= 1
    assert response_data["pending"] >= 1


@pytest.mark.asyncio
@test_steps("create_and_complete_todos", "get_stats", "verify_completion_counts")
async def test_get_todo_stats_after_completions(test_client: AsyncClient):
    """Test getting stats after completing some todos."""
    await _create_todos_with_statuses(test_client)
    
    list_response = await test_client.get("/api/v1/todos")
    todos = list_response.json()["todos"]
    
    pending_todo = next((t for t in todos if t["status"] == "pending"), None)
    if pending_todo:
        update_data = generate_todo_update_data(status=TodoStatusEnum.COMPLETED)
        await test_client.put(f"/api/v1/todos/{pending_todo['id']}", json=update_data)
    
    yield None
    
    response = await test_client.get("/api/v1/todos/stats")
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_stats_response_structure(response_data)
    assert response_data["completed"] >= 1
    assert response_data["total"] == (
        response_data["pending"] + 
        response_data["in_progress"] + 
        response_data["completed"]
    )

