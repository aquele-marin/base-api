from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum


class TodoStatus(str, Enum):
    """Status possíveis para um TODO"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    """Prioridades possíveis para um TODO"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo:
    """Entidade Todo - representa um item da lista de tarefas"""
    
    def __init__(
        self,
        title: str,
        description: Optional[str] = None,
        priority: TodoPriority = TodoPriority.MEDIUM,
        status: TodoStatus = TodoStatus.PENDING,
        due_date: Optional[datetime] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def mark_as_completed(self) -> None:
        """Marca a tarefa como completa"""
        self.status = TodoStatus.COMPLETED
        self.updated_at = datetime.utcnow()
    
    def mark_as_in_progress(self) -> None:
        """Marca a tarefa como em progresso"""
        self.status = TodoStatus.IN_PROGRESS
        self.updated_at = datetime.utcnow()
    
    def update_title(self, new_title: str) -> None:
        """Atualiza o título da tarefa"""
        self.title = new_title
        self.updated_at = datetime.utcnow()
    
    def update_description(self, new_description: Optional[str]) -> None:
        """Atualiza a descrição da tarefa"""
        self.description = new_description
        self.updated_at = datetime.utcnow()
    
    def update_priority(self, new_priority: TodoPriority) -> None:
        """Atualiza a prioridade da tarefa"""
        self.priority = new_priority
        self.updated_at = datetime.utcnow()
    
    def update_due_date(self, new_due_date: Optional[datetime]) -> None:
        """Atualiza a data de vencimento da tarefa"""
        self.due_date = new_due_date
        self.updated_at = datetime.utcnow()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Todo):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __repr__(self) -> str:
        return f"Todo(id={self.id}, title='{self.title}', status={self.status})"