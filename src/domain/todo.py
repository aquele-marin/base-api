from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from src.domain.todo_status import TodoStatus
from src.domain.todo_priority import TodoPriority

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(TodoStatus, nullable=False, default=TodoStatus.PENDING)
    priority = Column(TodoPriority, nullable=False, default=TodoPriority.MEDIUM)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def from_domain(cls, todo) -> "Todo":
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            priority=todo.priority,
            due_date=todo.due_date,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )
