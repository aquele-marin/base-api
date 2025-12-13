from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.resources import TodoResource
from src.api.schemas import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoListResponse,
    TodoStatsResponse,
)
from src.app import TodoService
from src.constants import TodoStatusEnum, TodoPriorityEnum
from src.infra import get_db_session
from src.repos import TodoRepository


todo_router = APIRouter()


def get_todo_service(session: AsyncSession = Depends(get_db_session)) -> TodoService:
    """Dependency para obter instância do TodoService"""
    repository = TodoRepository(session)
    return TodoService(repository, session)


def get_todo_resource(todo_service: TodoService = Depends(get_todo_service)) -> TodoResource:
    """Dependency para obter instância do TodoResource"""
    return TodoResource(todo_service)


@todo_router.post(
    "/todos",
    status_code=201,
    response_model=TodoResponse,
    summary="Criar novo TODO",
    description="Cria um novo item na lista de TODOs"
)
async def create_todo(
    todo_data: TodoCreateRequest,
    resource: TodoResource = Depends(get_todo_resource)
):
    """Cria um novo TODO"""
    try:
        return await resource.create(todo_data)
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
    status: Optional[TodoStatusEnum] = Query(None, description="Filtrar por status"),
    priority: Optional[TodoPriorityEnum] = Query(None, description="Filtrar por prioridade"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de itens"),
    offset: int = Query(0, ge=0, description="Número de itens a pular"),
    resource: TodoResource = Depends(get_todo_resource)
):
    """Lista TODOs com filtros opcionais"""
    try:
        return await resource.list(status, priority, limit, offset)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@todo_router.get(
    "/todos/stats",
    response_model=TodoStatsResponse,
    summary="Estatísticas dos TODOs",
    description="Retorna estatísticas gerais dos TODOs"
)
async def get_todo_stats(
    resource: TodoResource = Depends(get_todo_resource)
):
    """Retorna estatísticas dos TODOs"""
    try:
        return await resource.get_stats()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@todo_router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    summary="Obter TODO por ID",
    description="Busca um TODO específico pelo seu ID"
)
async def get_todo(
    todo_id: UUID,
    resource: TodoResource = Depends(get_todo_resource)
):
    """Busca um TODO pelo ID"""
    try:
        todo = await resource.get_by_id(todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="TODO not found")
        return todo
    except Exception:
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
    resource: TodoResource = Depends(get_todo_resource)
):
    """Atualiza um TODO existente"""
    try:
        return await resource.update(todo_id, todo_data)
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
    resource: TodoResource = Depends(get_todo_resource)
):
    """Deleta um TODO"""
    try:
        deleted = await resource.delete(todo_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="TODO not found")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")