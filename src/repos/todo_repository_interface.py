from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.todo import Todo, TodoStatus, TodoPriority


class TodoRepositoryInterface(ABC):
    """Interface do repositório de TODOs"""
    
    @abstractmethod
    async def create(self, todo: Todo) -> Todo:
        """Cria um novo TODO"""
        pass
    
    @abstractmethod
    async def get_by_id(self, todo_id: UUID) -> Optional[Todo]:
        """Busca um TODO pelo ID"""
        pass
    
    @abstractmethod
    async def get_all(
        self, 
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Todo]:
        """Busca todos os TODOs com filtros opcionais"""
        pass
    
    @abstractmethod
    async def update(self, todo: Todo) -> Todo:
        """Atualiza um TODO existente"""
        pass
    
    @abstractmethod
    async def delete(self, todo_id: UUID) -> bool:
        """Deleta um TODO pelo ID"""
        pass
    
    @abstractmethod
    async def count(
        self,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None
    ) -> int:
        """Conta o número de TODOs com filtros opcionais"""
        pass