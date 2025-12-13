from typing import List, Optional
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain import Todo, TodoStatus, TodoPriority


class TodoRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def _get_status_by_value(self, value: str) -> Optional[TodoStatus]:
        """
        Busca um TodoStatus pelo valor.
        """
        stmt = select(TodoStatus).where(TodoStatus.value == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def _get_priority_by_value(self, value: str) -> Optional[TodoPriority]:
        """
        Busca um TodoPriority pelo valor.
        """
        stmt = select(TodoPriority).where(TodoPriority.value == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ) -> Todo:
        """Cria um novo TODO"""
        status_model = await self._get_status_by_value(status)
        if not status_model:
            raise ValueError(f"Status '{status}' not found")
        
        priority_model = await self._get_priority_by_value(priority)
        if not priority_model:
            raise ValueError(f"Priority '{priority}' not found")
        
        todo = Todo(
            title=title,
            description=description,
            status_id=status_model.id,
            priority_id=priority_model.id,
            due_date=due_date
        )

        self.session.add(todo)
        await self.session.commit()
        return todo
    
    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """Busca um TODO pelo ID"""
        stmt = select(Todo).where(Todo.id == todo_id)
        result = await self.session.execute(stmt)
        todo_model = result.scalar_one_or_none()
        return todo_model
    
    async def get_all(
        self, 
        status: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Todo]:
        """Busca todos os TODOs com filtros opcionais"""
        stmt = select(Todo)
        
        if status:
            status_model = await self._get_status_by_value(status)
            if status_model:
                stmt = stmt.where(Todo.status_id == status_model.id)
        
        if priority:
            priority_model = await self._get_priority_by_value(priority)
            if priority_model:
                stmt = stmt.where(Todo.priority_id == priority_model.id)
        
        stmt = stmt.order_by(Todo.created_at.desc()).offset(offset).limit(limit)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def delete(self, todo_id: UUID) -> bool:
        stmt = delete(Todo).where(Todo.id == todo_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def count(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> int:
        """Conta TODOs com filtros opcionais"""
        stmt = select(func.count(Todo.id))
        
        if status:
            status_model = await self._get_status_by_value(status)
            if status_model:
                stmt = stmt.where(Todo.status_id == status_model.id)
        
        if priority:
            priority_model = await self._get_priority_by_value(priority)
            if priority_model:
                stmt = stmt.where(Todo.priority_id == priority_model.id)
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0