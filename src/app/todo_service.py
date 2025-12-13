from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import Todo
from src.repos import TodoRepository


class TodoService:
    def __init__(self, todo_repository: TodoRepository, session: AsyncSession):
        self.todo_repository = todo_repository
        self.session = session
    
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
        
        todo = await self.todo_repository.create(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority,
            due_date=due_date
        )
        await self.session.commit()
        return todo
    
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
    
    async def update_todo(
        self,
        todo_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Atualiza um TODO existente"""
        todo = await self.todo_repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"TODO with id {todo_id} not found")
        
        if title:
            todo.title = title
        if description:
            todo.description = description
        if status:
            status_model = await self.todo_repository._get_status_by_value(status)
            if not status_model:
                raise ValueError(f"Status '{status}' not found")
            todo.status = status_model
        if priority:
            priority_model = await self.todo_repository._get_priority_by_value(priority)
            if not priority_model:
                raise ValueError(f"Priority '{priority}' not found")
            todo.priority = priority_model
        if due_date:
            todo.due_date = due_date
        
        await self.session.commit()
        return todo.to_dict()
    
    async def delete_todo(self, todo_id: UUID) -> bool:
        todo = await self.todo_repository.get_by_id(todo_id)
        if not todo:
            raise ValueError(f"TODO with id {todo_id} not found")
        
        result = await self.todo_repository.delete(todo_id)
        await self.session.commit()
        return result
    
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