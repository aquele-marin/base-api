from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.todo import Todo, TodoStatus, TodoPriority
from src.repos.todo_repository_interface import TodoRepositoryInterface
from src.infra.database.models import TodoModel


class SqlAlchemyTodoRepository(TodoRepositoryInterface):
    """Implementação SQLAlchemy do repositório de TODOs"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, todo: Todo) -> Todo:
        """Cria um novo TODO"""
        todo_model = TodoModel.from_domain(todo)
        self.session.add(todo_model)
        await self.session.commit()
        await self.session.refresh(todo_model)
        return todo_model.to_domain()
    
    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """Busca um TODO pelo ID"""
        stmt = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(stmt)
        todo_model = result.scalar_one_or_none()
        
        if todo_model:
            return todo_model.to_domain()
        return None
    
    async def get_all(
        self, 
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Todo]:
        """Busca todos os TODOs com filtros opcionais"""
        stmt = select(TodoModel)
        
        if status:
            stmt = stmt.where(TodoModel.status == status)
        
        if priority:
            stmt = stmt.where(TodoModel.priority == priority)
        
        stmt = stmt.order_by(TodoModel.created_at.desc()).offset(offset).limit(limit)
        
        result = await self.session.execute(stmt)
        todo_models = result.scalars().all()
        
        return [todo_model.to_domain() for todo_model in todo_models]
    
    async def update(self, todo: Todo) -> Todo:
        """Atualiza um TODO existente"""
        stmt = select(TodoModel).where(TodoModel.id == todo.id)
        result = await self.session.execute(stmt)
        todo_model = result.scalar_one_or_none()
        
        if not todo_model:
            raise ValueError(f"TODO with id {todo.id} not found")
        
        todo_model.update_from_domain(todo)
        await self.session.commit()
        await self.session.refresh(todo_model)
        return todo_model.to_domain()
    
    async def delete(self, todo_id: UUID) -> bool:
        """Deleta um TODO pelo ID"""
        stmt = delete(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        return result.rowcount > 0
    
    async def count(
        self,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None
    ) -> int:
        """Conta o número de TODOs com filtros opcionais"""
        stmt = select(func.count(TodoModel.id))
        
        if status:
            stmt = stmt.where(TodoModel.status == status)
        
        if priority:
            stmt = stmt.where(TodoModel.priority == priority)
        
        result = await self.session.execute(stmt)
        return result.scalar() or 0