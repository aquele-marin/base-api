from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from src.infra.database.connection import Base
from src.domain.todo import TodoStatus, TodoPriority, Todo


class TodoModel(Base):
    """Modelo SQLAlchemy para a tabela de TODOs"""
    
    __tablename__ = "todos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatus), nullable=False, default=TodoStatus.PENDING)
    priority = Column(Enum(TodoPriority), nullable=False, default=TodoPriority.MEDIUM)
    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_domain(self) -> Todo:
        """Converte o modelo SQLAlchemy para a entidade de domínio"""
        return Todo(
            id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            priority=self.priority,
            due_date=self.due_date,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain(cls, todo: Todo) -> "TodoModel":
        """Cria um modelo SQLAlchemy a partir de uma entidade de domínio"""
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
    
    def update_from_domain(self, todo: Todo) -> None:
        """Atualiza o modelo com os dados da entidade de domínio"""
        self.title = todo.title
        self.description = todo.description
        self.status = todo.status
        self.priority = todo.priority
        self.due_date = todo.due_date
        self.updated_at = todo.updated_at