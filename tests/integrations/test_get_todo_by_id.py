import pytest
from uuid import UUID
from pytest_steps import test_steps
from httpx import AsyncClient

from tests.generator import generate_todo_create_data
from tests.tools.response_helpers import assert_todo_response_structure
from tests.utils import extract_todo_id_from_response, assert_todo_content


@pytest.mark.asyncio
@test_steps("create_todo", "get_todo_by_id", "verify_response_structure", "verify_todo_data")
async def test_get_todo_by_id_success(test_client: AsyncClient):
    """Test getting a todo by its ID."""
    todo_data = generate_todo_create_data(title="Get Todo Test")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    response = await test_client.get(f"/api/v1/todos/{todo_id}")
    
    yield response
    
    assert response.status_code == 200
    
    yield response
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    
    yield response_data
    
    assert_todo_content(response_data, {"title": todo_data["title"]})


@pytest.mark.asyncio
@test_steps("attempt_get_nonexistent_todo", "verify_not_found_response")
async def test_get_todo_by_id_not_found(test_client: AsyncClient):
    """Test getting a todo that doesn't exist."""
    fake_id = UUID("00000000-0000-0000-0000-000000000000")
    
    yield fake_id
    
    response = await test_client.get(f"/api/v1/todos/{fake_id}")
    
    yield response
    
    assert response.status_code == 404


@pytest.mark.asyncio
@test_steps("attempt_get_with_invalid_uuid", "verify_bad_request_response")
async def test_get_todo_by_id_invalid_uuid(test_client: AsyncClient):
    """Test getting a todo with invalid UUID format."""
    invalid_id = "not-a-valid-uuid"
    
    yield invalid_id
    
    response = await test_client.get(f"/api/v1/todos/{invalid_id}")
    
    yield response
    
    assert response.status_code == 422


@pytest.mark.asyncio
@test_steps("create_todo_with_full_data", "get_todo_verify_all_fields")
async def test_get_todo_with_all_fields(test_client: AsyncClient):
    """Test getting a todo with all fields populated."""
    from tests.generator import generate_future_due_date
    from src.constants import TodoPriorityEnum
    
    todo_data = generate_todo_create_data(
        title="Complete Todo",
        description="Full description",
        priority=TodoPriorityEnum.HIGH,
        due_date=generate_future_due_date(days=10)
    )
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    response = await test_client.get(f"/api/v1/todos/{todo_id}")
    
    yield response
    
    assert response.status_code == 200
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert response_data["description"] == todo_data["description"]
    assert response_data["priority"] == todo_data["priority"]
    assert "due_date" in response_data

