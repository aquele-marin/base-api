from typing import Dict, Any
from uuid import UUID


def extract_todo_id_from_response(response_data: Dict[str, Any]) -> UUID:
    """Extract todo ID from API response."""
    return UUID(response_data["id"])


def assert_todo_fields_present(response_data: Dict[str, Any]) -> None:
    """Assert all required todo fields are present in response."""
    required_fields = ["id", "title", "status", "priority", "created_at", "updated_at"]
    for field in required_fields:
        assert field in response_data, f"Missing required field: {field}"


def assert_todo_content(response_data: Dict[str, Any], expected_data: Dict[str, Any]) -> None:
    """Assert todo response matches expected data."""
    if "title" in expected_data:
        assert response_data["title"] == expected_data["title"]
    if "description" in expected_data:
        assert response_data["description"] == expected_data["description"]
    if "priority" in expected_data:
        assert response_data["priority"] == expected_data["priority"]
    if "status" in expected_data:
        assert response_data["status"] == expected_data["status"]

