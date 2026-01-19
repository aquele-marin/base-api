import pytest
from uuid import UUID
from pytest_steps import test_steps
from httpx import AsyncClient
from src.constants import TodoStatusEnum, TodoPriorityEnum

from tests.generator import generate_todo_create_data, generate_todo_update_data
from tests.tools.response_helpers import assert_todo_response_structure
from tests.utils import extract_todo_id_from_response, assert_todo_content


@pytest.mark.asyncio
@test_steps("create_todo", "update_todo_title", "verify_title_updated")
async def test_update_todo_title(test_client: AsyncClient):
    """Test updating a todo's title."""
    todo_data = generate_todo_create_data(title="Original Title")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    update_data = generate_todo_update_data(title="Updated Title")
    response = await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert response_data["title"] == "Updated Title"


@pytest.mark.asyncio
@test_steps("create_todo", "update_todo_status", "verify_status_updated")
async def test_update_todo_status(test_client: AsyncClient):
    """Test updating a todo's status."""
    todo_data = generate_todo_create_data(title="Status Update Todo")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    update_data = generate_todo_update_data(status=TodoStatusEnum.IN_PROGRESS)
    response = await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert response_data["status"] == "in_progress"


@pytest.mark.asyncio
@test_steps("create_todo", "update_todo_priority", "verify_priority_updated")
async def test_update_todo_priority(test_client: AsyncClient):
    """Test updating a todo's priority."""
    todo_data = generate_todo_create_data(title="Priority Update Todo", priority=TodoPriorityEnum.LOW)
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    update_data = generate_todo_update_data(priority=TodoPriorityEnum.HIGH)
    response = await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert response_data["priority"] == "high"


@pytest.mark.asyncio
@test_steps("create_todo", "update_multiple_fields", "verify_all_fields_updated")
async def test_update_todo_multiple_fields(test_client: AsyncClient):
    """Test updating multiple fields of a todo."""
    from tests.generator import generate_future_due_date
    
    todo_data = generate_todo_create_data(title="Multi Update Todo")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    update_data = generate_todo_update_data(
        title="Multi Updated Title",
        description="Updated description",
        status=TodoStatusEnum.COMPLETED,
        priority=TodoPriorityEnum.HIGH,
        due_date=generate_future_due_date(days=5)
    )
    response = await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert response_data["title"] == "Multi Updated Title"
    assert response_data["description"] == "Updated description"
    assert response_data["status"] == "completed"
    assert response_data["priority"] == "high"


@pytest.mark.asyncio
@test_steps("attempt_update_nonexistent_todo", "verify_not_found_response")
async def test_update_todo_not_found(test_client: AsyncClient):
    """Test updating a todo that doesn't exist."""
    fake_id = UUID("00000000-0000-0000-0000-000000000000")
    update_data = generate_todo_update_data(title="Should Fail")
    
    yield fake_id
    
    response = await test_client.put(f"/api/v1/todos/{fake_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 404


@pytest.mark.asyncio
@test_steps("create_todo", "update_with_invalid_data", "verify_validation_error")
async def test_update_todo_with_invalid_title(test_client: AsyncClient):
    """Test updating a todo with invalid title."""
    todo_data = generate_todo_create_data(title="Valid Todo")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    update_data = {"title": ""}
    response = await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 422


@pytest.mark.asyncio
@test_steps("create_todo", "mark_as_completed", "verify_completion")
async def test_complete_todo(test_client: AsyncClient):
    """Test completing a todo by updating its status."""
    todo_data = generate_todo_create_data(title="Todo to Complete")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    update_data = generate_todo_update_data(status=TodoStatusEnum.COMPLETED)
    response = await test_client.put(f"/api/v1/todos/{todo_id}", json=update_data)
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert response_data["status"] == "completed"

