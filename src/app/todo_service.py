from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.domain import Todo
from src.repos import TodoRepository


class TodoService:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository
    
    async def create_todo(
        self,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Cria um novo TODO"""
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")
        
        return await self.todo_repository.create(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority,
            due_date=due_date
        )
    
    async def get_todo_by_id(self, todo_id: UUID) -> Optional[Todo]:
        return await self.todo_repository.get_by_id(todo_id)
    
    async def get_todos(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Todo]:
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
    
    async def delete_todo(self, todo_id: UUID) -> bool:
        todo = await self.todo_repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"TODO with id {todo_id} not found")
        
        return await self.todo_repository.delete(todo_id)
    
    async def get_todo_stats(self) -> dict:
        """Retorna estatísticas dos TODOs"""
        total = await self.todo_repository.count()
        pending = await self.todo_repository.count(status="pending")
        in_progress = await self.todo_repository.count(status="in_progress")
        completed = await self.todo_repository.count(status="completed")
        
        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed
        }