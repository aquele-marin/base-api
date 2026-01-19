import pytest
from pytest_steps import test_steps
from httpx import AsyncClient
from src.constants import TodoPriorityEnum

from tests.generator import generate_todo_create_data
from tests.tools.response_helpers import assert_todo_response_structure
from tests.utils import assert_todo_content


@pytest.mark.asyncio
@test_steps("create_todo_with_minimal_data", "verify_response_structure", "verify_todo_created")
async def test_create_todo_with_minimal_data(test_client: AsyncClient):
    """Test creating a todo with only required fields."""
    todo_data = generate_todo_create_data(title="Minimal Todo")
    
    response = await test_client.post("/api/v1/todos", json=todo_data)
    
    yield response
    
    assert response.status_code == 201
    
    yield response
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert_todo_content(response_data, {"title": todo_data["title"], "priority": todo_data["priority"]})


@pytest.mark.asyncio
@test_steps("create_todo_with_all_fields", "verify_response_contains_all_data")
async def test_create_todo_with_all_fields(test_client: AsyncClient):
    """Test creating a todo with all fields provided."""
    from tests.generator import generate_future_due_date
    
    todo_data = generate_todo_create_data(
        title="Complete Todo",
        description="This is a complete todo description",
        priority=TodoPriorityEnum.HIGH,
        due_date=generate_future_due_date(days=14)
    )
    
    response = await test_client.post("/api/v1/todos", json=todo_data)
    
    yield response
    
    assert response.status_code == 201
    
    response_data = response.json()
    assert_todo_response_structure(response_data)
    assert_todo_content(response_data, {
        "title": todo_data["title"],
        "description": todo_data["description"],
        "priority": todo_data["priority"]
    })


@pytest.mark.asyncio
@test_steps("create_todo_with_different_priorities", "verify_priority_assigned")
async def test_create_todo_with_different_priorities(test_client: AsyncClient):
    """Test creating todos with different priority levels."""
    for priority in [TodoPriorityEnum.LOW, TodoPriorityEnum.MEDIUM, TodoPriorityEnum.HIGH]:
        todo_data = generate_todo_create_data(
            title=f"Todo with {priority.value} priority",
            priority=priority
        )
        
        response = await test_client.post("/api/v1/todos", json=todo_data)
        
        yield response
        
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["priority"] == priority.value


@pytest.mark.asyncio
@test_steps("create_todo_with_invalid_data", "verify_error_response")
async def test_create_todo_with_invalid_title(test_client: AsyncClient):
    """Test creating a todo with invalid title."""
    todo_data = generate_todo_create_data(title="")
    
    response = await test_client.post("/api/v1/todos", json=todo_data)
    
    yield response
    
    assert response.status_code == 422


@pytest.mark.asyncio
@test_steps("create_todo_with_long_title", "verify_error_response")
async def test_create_todo_with_title_too_long(test_client: AsyncClient):
    """Test creating a todo with title exceeding max length."""
    todo_data = generate_todo_create_data(title="a" * 201)
    
    response = await test_client.post("/api/v1/todos", json=todo_data)
    
    yield response
    
    assert response.status_code == 422


@pytest.mark.asyncio
@test_steps("create_todo_without_title", "verify_error_response")
async def test_create_todo_without_title(test_client: AsyncClient):
    """Test creating a todo without required title field."""
    todo_data = {"description": "Todo without title"}
    
    response = await test_client.post("/api/v1/todos", json=todo_data)
    
    yield response
    
    assert response.status_code == 422

