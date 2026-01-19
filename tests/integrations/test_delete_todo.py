import pytest
from uuid import UUID
from pytest_steps import test_steps
from httpx import AsyncClient

from tests.generator import generate_todo_create_data
from tests.utils import extract_todo_id_from_response


@pytest.mark.asyncio
@test_steps("create_todo", "delete_todo", "verify_deletion", "verify_todo_removed")
async def test_delete_todo_success(test_client: AsyncClient):
    """Test deleting a todo successfully."""
    todo_data = generate_todo_create_data(title="Todo to Delete")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    response = await test_client.delete(f"/api/v1/todos/{todo_id}")
    
    yield response
    
    assert response.status_code == 204
    
    yield response
    
    get_response = await test_client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
@test_steps("attempt_delete_nonexistent_todo", "verify_not_found_response")
async def test_delete_todo_not_found(test_client: AsyncClient):
    """Test deleting a todo that doesn't exist."""
    fake_id = UUID("00000000-0000-0000-0000-000000000000")
    
    yield fake_id
    
    response = await test_client.delete(f"/api/v1/todos/{fake_id}")
    
    yield response
    
    assert response.status_code == 404


@pytest.mark.asyncio
@test_steps("create_multiple_todos", "delete_one", "verify_others_remain")
async def test_delete_todo_preserves_others(test_client: AsyncClient):
    """Test that deleting one todo doesn't affect others."""
    todo1_data = generate_todo_create_data(title="Todo 1")
    todo2_data = generate_todo_create_data(title="Todo 2")
    
    create_response1 = await test_client.post("/api/v1/todos", json=todo1_data)
    create_response2 = await test_client.post("/api/v1/todos", json=todo2_data)
    
    todo1_id = extract_todo_id_from_response(create_response1.json())
    todo2_id = extract_todo_id_from_response(create_response2.json())
    
    yield [todo1_id, todo2_id]
    
    delete_response = await test_client.delete(f"/api/v1/todos/{todo1_id}")
    assert delete_response.status_code == 204
    
    yield delete_response
    
    get_response1 = await test_client.get(f"/api/v1/todos/{todo1_id}")
    get_response2 = await test_client.get(f"/api/v1/todos/{todo2_id}")
    
    yield [get_response1, get_response2]
    
    assert get_response1.status_code == 404
    assert get_response2.status_code == 200


@pytest.mark.asyncio
@test_steps("create_todo", "delete_todo", "attempt_redelete", "verify_error")
async def test_delete_todo_twice(test_client: AsyncClient):
    """Test that deleting a todo twice returns not found."""
    todo_data = generate_todo_create_data(title="Double Delete Todo")
    create_response = await test_client.post("/api/v1/todos", json=todo_data)
    todo_id = extract_todo_id_from_response(create_response.json())
    
    yield todo_id
    
    first_delete = await test_client.delete(f"/api/v1/todos/{todo_id}")
    assert first_delete.status_code == 204
    
    yield first_delete
    
    second_delete = await test_client.delete(f"/api/v1/todos/{todo_id}")
    
    yield second_delete
    
    assert second_delete.status_code == 404


@pytest.mark.asyncio
@test_steps("attempt_delete_with_invalid_uuid", "verify_bad_request")
async def test_delete_todo_invalid_uuid(test_client: AsyncClient):
    """Test deleting a todo with invalid UUID format."""
    invalid_id = "not-a-valid-uuid"
    
    yield invalid_id
    
    response = await test_client.delete(f"/api/v1/todos/{invalid_id}")
    
    yield response
    
    assert response.status_code == 422

