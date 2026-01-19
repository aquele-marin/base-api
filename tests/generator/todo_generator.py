from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

from src.constants import TodoPriorityEnum, TodoStatusEnum


def generate_todo_create_data(
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[TodoPriorityEnum] = None,
    due_date: Optional[datetime] = None
) -> dict:
    """Generate mock data for todo creation request."""
    return {
        "title": title or f"Test Todo {uuid4().hex[:8]}",
        "description": description or f"Test description for {title or 'todo'}",
        "priority": (priority or TodoPriorityEnum.MEDIUM).value,
        "due_date": due_date.isoformat() if due_date else None
    }


def generate_todo_update_data(
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[TodoPriorityEnum] = None,
    status: Optional[TodoStatusEnum] = None,
    due_date: Optional[datetime] = None
) -> dict:
    """Generate mock data for todo update request."""
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if priority is not None:
        data["priority"] = priority.value
    if status is not None:
        data["status"] = status.value
    if due_date is not None:
        data["due_date"] = due_date.isoformat()
    return data


def generate_future_due_date(days: int = 7) -> datetime:
    """Generate a future date for due_date."""
    return datetime.utcnow() + timedelta(days=days)


def generate_past_due_date(days: int = 7) -> datetime:
    """Generate a past date for due_date."""
    return datetime.utcnow() - timedelta(days=days)

