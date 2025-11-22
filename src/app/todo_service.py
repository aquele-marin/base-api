from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain import Todo, TodoStatus, TodoPriority
from src.repos import TodoRepository


class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository
    
    async def create_todo(
        self,
        title: str,
        description: Optional[str] = None,
        priority: TodoPriority = TodoPriority.MEDIUM,
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Cria um novo TODO"""
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")
        
        todo = Todo(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority,
            due_date=due_date
        )
        
        return await self.todo_repository.create(todo)
    
    async def get_todo_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """Busca um TODO pelo ID"""
        return await self.todo_repository.get_by_id(todo_id)
    
    async def get_todos(
        self,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Todo]:
        """Lista TODOs com filtros opcionais"""
        if limit <= 0:
            raise ValueError("Limit must be greater than 0")
        
        if offset < 0:
            raise ValueError("Offset must be greater than or equal to 0")
        
        return await self.todo_repository.get_all(
            status=status,
            priority=priority,
            limit=limit,
            offset=offset
        )
    
    async def update_todo(
        self,
        todo_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[TodoPriority] = None,
        status: Optional[TodoStatus] = None,
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Atualiza um TODO existente"""
        todo = await self.todo_repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"TODO with id {todo_id} not found")
        
        if title is not None:
            if not title or title.strip() == "":
                raise ValueError("Title cannot be empty")
            todo.update_title(title.strip())
        
        if description is not None:
            todo.update_description(description.strip() if description else None)
        
        if priority is not None:
            todo.update_priority(priority)
        
        if status is not None:
            if status == TodoStatus.COMPLETED:
                todo.mark_as_completed()
            elif status == TodoStatus.IN_PROGRESS:
                todo.mark_as_in_progress()
            else:
                todo.status = status
                todo.updated_at = datetime.utcnow()
        
        if due_date is not None:
            todo.update_due_date(due_date)
        
        return await self.todo_repository.update(todo)
    
    async def delete_todo(self, todo_id: UUID) -> bool:
        """Deleta um TODO"""
        todo = await self.todo_repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"TODO with id {todo_id} not found")
        
        return await self.todo_repository.delete(todo_id)
    
    async def mark_todo_as_completed(self, todo_id: UUID) -> Todo:
        """Marca um TODO como completo"""
        return await self.update_todo(todo_id, status=TodoStatus.COMPLETED)
    
    async def mark_todo_as_in_progress(self, todo_id: UUID) -> Todo:
        """Marca um TODO como em progresso"""
        return await self.update_todo(todo_id, status=TodoStatus.IN_PROGRESS)
    
    async def get_todo_stats(self) -> dict:
        """Retorna estatísticas dos TODOs"""
        total = await self.todo_repository.count()
        pending = await self.todo_repository.count(status=TodoStatus.PENDING)
        in_progress = await self.todo_repository.count(status=TodoStatus.IN_PROGRESS)
        completed = await self.todo_repository.count(status=TodoStatus.COMPLETED)
        
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed
        }