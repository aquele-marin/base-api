from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.todo_schemas import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoStatusUpdateRequest,
    TodoResponse,
    TodoListResponse,
    TodoStatsResponse,
    ErrorResponse
)
from src.app.todo_service import TodoService
from src.domain.todo import TodoStatus, TodoPriority
from src.infra.database.connection import get_db_session
from src.infra.database.todo_repository import SqlAlchemyTodoRepository


todo_router = APIRouter()


def get_todo_service(session: AsyncSession = Depends(get_db_session)) -> TodoService:
    """Dependency para obter o serviço de TODOs"""
    repository = SqlAlchemyTodoRepository(session)
    return TodoService(repository)


@todo_router.post(
    "/todos", 
    response_model=TodoResponse,
    status_code=201,
    summary="Criar novo TODO",
    description="Cria um novo item na lista de TODOs"
)
async def create_todo(
    todo_data: TodoCreateRequest,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Cria um novo TODO"""
    try:
        todo = await todo_service.create_todo(
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            due_date=todo_data.due_date
        )
        return TodoResponse.from_domain(todo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@todo_router.get(
    "/todos",
    response_model=TodoListResponse,
    summary="Listar TODOs",
    description="Lista todos os TODOs com filtros opcionais"
)
async def get_todos(
    status: Optional[TodoStatus] = Query(None, description="Filtrar por status"),
    priority: Optional[TodoPriority] = Query(None, description="Filtrar por prioridade"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de itens"),
    offset: int = Query(0, ge=0, description="Número de itens a pular"),
    todo_service: TodoService = Depends(get_todo_service)
):
    """Lista TODOs com filtros opcionais"""
    try:
        todos = await todo_service.get_todos(
            status=status,
            priority=priority,
            limit=limit,
            offset=offset
        )
        todo_responses = [TodoResponse.from_domain(todo) for todo in todos]
        
        return TodoListResponse(
            todos=todo_responses,
            total=len(todo_responses),
            limit=limit,
            offset=offset
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@todo_router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    summary="Obter TODO por ID",
    description="Busca um TODO específico pelo seu ID"
)
async def get_todo(
    todo_id: UUID,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Busca um TODO pelo ID"""
    try:
        todo = await todo_service.get_todo_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="TODO not found")
        return TodoResponse.from_domain(todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@todo_router.put(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    summary="Atualizar TODO",
    description="Atualiza um TODO existente"
)
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdateRequest,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Atualiza um TODO existente"""
    try:
        todo = await todo_service.update_todo(
            todo_id=todo_id,
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            status=todo_data.status,
            due_date=todo_data.due_date
        )
        return TodoResponse.from_domain(todo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@todo_router.patch(
    "/todos/{todo_id}/status",
    response_model=TodoResponse,
    summary="Atualizar status do TODO",
    description="Atualiza apenas o status de um TODO"
)
async def update_todo_status(
    todo_id: UUID,
    status_data: TodoStatusUpdateRequest,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Atualiza apenas o status de um TODO"""
    try:
        todo = await todo_service.update_todo(
            todo_id=todo_id,
            status=status_data.status
        )
        return TodoResponse.from_domain(todo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@todo_router.delete(
    "/todos/{todo_id}",
    status_code=204,
    summary="Deletar TODO",
    description="Deleta um TODO existente"
)
async def delete_todo(
    todo_id: UUID,
    todo_service: TodoService = Depends(get_todo_service)
):
    """Deleta um TODO"""
    try:
        deleted = await todo_service.delete_todo(todo_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="TODO not found")
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@todo_router.get(
    "/todos/stats",
    response_model=TodoStatsResponse,
    summary="Estatísticas dos TODOs",
    description="Retorna estatísticas gerais dos TODOs"
)
async def get_todo_stats(
    todo_service: TodoService = Depends(get_todo_service)
):
    """Retorna estatísticas dos TODOs"""
    try:
        stats = await todo_service.get_todo_stats()
        return TodoStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")