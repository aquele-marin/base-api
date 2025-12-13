from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infra import Base


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status_id = Column(Integer, ForeignKey("todo_statuses.id"), nullable=False)
    priority_id = Column(Integer, ForeignKey("todo_priorities.id"), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    status = relationship("TodoStatus", back_populates="todos", lazy="joined")
    priority = relationship("TodoPriority", back_populates="todos", lazy="joined")

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}')>"
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.title == other
        if isinstance(other, Todo):
            return self.id == other.id
        return False
    
    def to_dict(self) -> dict:
        """
        Convert Todo instance to dictionary.

        Returns:
            dict: Dictionary with id, title, description, status, priority, due_date, created_at and updated_at.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }