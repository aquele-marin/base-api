from typing import Any, Dict


def assert_todo_response_structure(response_data: Dict[str, Any]) -> None:
    """
    Assert that a todo response has the expected structure.

    Args:
        response_data: Response data dictionary to validate.

    Raises:
        AssertionError: If response structure is invalid.
    """
    required_fields = ["id", "title", "status", "priority", "created_at", "updated_at"]

    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"

    assert isinstance(response_data["id"], str), "ID should be a string (UUID)"
    assert isinstance(response_data["title"], str), "Title should be a string"
    assert response_data["title"], "Title should not be empty"


def assert_todo_list_response_structure(response_data: Dict[str, Any]) -> None:
    """
    Assert that a todo list response has the expected structure.

    Args:
        response_data: Response data dictionary to validate.

    Raises:
        AssertionError: If response structure is invalid.
    """
    assert "todos" in response_data, "Missing 'todos' field"
    assert "total" in response_data, "Missing 'total' field"
    assert "limit" in response_data, "Missing 'limit' field"
    assert "offset" in response_data, "Missing 'offset' field"

    assert isinstance(response_data["todos"], list), "todos should be a list"
    assert isinstance(response_data["total"], int), "total should be an integer"
    assert isinstance(response_data["limit"], int), "limit should be an integer"
    assert isinstance(response_data["offset"], int), "offset should be an integer"

    assert response_data["total"] >= 0, "total should be non-negative"
    assert response_data["limit"] > 0, "limit should be positive"


def assert_todo_stats_response_structure(response_data: Dict[str, Any]) -> None:
    """
    Assert that a todo stats response has the expected structure.

    Args:
        response_data: Response data dictionary to validate.

    Raises:
        AssertionError: If response structure is invalid.
    """
    required_fields = ["total", "pending", "in_progress", "completed"]

    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"
        assert isinstance(response_data[field], int), f"{field} should be an integer"
        assert response_data[field] >= 0, f"{field} should be non-negative"
