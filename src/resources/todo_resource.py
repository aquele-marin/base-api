from typing import Optional
from uuid import UUID

from src.api.schemas import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoStatusUpdateRequest,
    TodoResponse,
    TodoListResponse,
    TodoStatsResponse,
)
from src.app import TodoService
from src.constants import TodoStatusEnum, TodoPriorityEnum


class TodoResource:
    """Resource layer para orquestração de operações de TODO"""

    def __init__(self, todo_service: TodoService):
        self.todo_service = todo_service

    async def create(self, request: TodoCreateRequest) -> TodoResponse:
        """Cria um novo TODO"""
        priority_value = (
            request.priority.value
            if isinstance(request.priority, TodoPriorityEnum)
            else request.priority
        )

        todo = await self.todo_service.create_todo(
            title=request.title,
            description=request.description,
            priority=priority_value,
            due_date=request.due_date,
        )
        return TodoResponse.from_domain(todo=todo)

    async def get_by_id(self, todo_id: UUID) -> Optional[TodoResponse]:
        """Busca um TODO pelo ID"""
        todo = await self.todo_service.get_todo_by_id(todo_id)
        if not todo:
            return None
        return TodoResponse.from_domain(todo=todo)

    async def list(
        self,
        status: Optional[TodoStatusEnum],
        priority: Optional[TodoPriorityEnum],
        limit: int,
        offset: int,
    ) -> TodoListResponse:
        """Lista TODOs com filtros opcionais"""
        status_value = status.value if status else None
        priority_value = priority.value if priority else None

        todos = await self.todo_service.get_todos(
            status=status_value, priority=priority_value, limit=limit, offset=offset
        )

        return TodoListResponse(
            todos=[TodoResponse.from_domain(todo=todo) for todo in todos],
            total=len(todos),
            limit=limit,
            offset=offset,
        )

    async def update(self, todo_id: UUID, request: TodoUpdateRequest) -> TodoResponse:
        """Atualiza um TODO existente"""
        status_value = (
            request.status.value
            if request.status and isinstance(request.status, TodoStatusEnum)
            else None
        )
        priority_value = (
            request.priority.value
            if request.priority and isinstance(request.priority, TodoPriorityEnum)
            else None
        )

        todo = await self.todo_service.update_todo(
            todo_id=todo_id,
            title=request.title,
            description=request.description,
            status=status_value,
            priority=priority_value,
            due_date=request.due_date,
        )
        return TodoResponse.from_domain(todo=todo)

    async def update_status(
        self, todo_id: UUID, request: TodoStatusUpdateRequest
    ) -> TodoResponse:
        """Atualiza apenas o status de um TODO"""
        status_value = (
            request.status.value
            if isinstance(request.status, TodoStatusEnum)
            else request.status
        )

        todo = await self.todo_service.update_todo(todo_id=todo_id, status=status_value)
        return TodoResponse.from_domain(todo=todo)

    async def delete(self, todo_id: UUID) -> bool:
        """Deleta um TODO"""
        return await self.todo_service.delete_todo(todo_id)

    async def get_stats(self) -> TodoStatsResponse:
        """Retorna estatísticas dos TODOs"""
        stats = await self.todo_service.get_todo_stats()
        return TodoStatsResponse(**stats)
