from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.constants import TodoStatusEnum, TodoPriorityEnum


# Schemas de entrada (Request)
class TodoCreateRequest(BaseModel):
    """Schema para criação de TODO"""
    title: str = Field(..., min_length=1, max_length=200, description="Título do TODO")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição detalhada do TODO")
    priority: TodoPriorityEnum = Field(TodoPriorityEnum.MEDIUM, description="Prioridade do TODO")
    due_date: Optional[datetime] = Field(None, description="Data de vencimento do TODO")


class TodoUpdateRequest(BaseModel):
    """Schema para atualização de TODO"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Novo título do TODO")
    description: Optional[str] = Field(None, max_length=1000, description="Nova descrição do TODO")
    priority: Optional[TodoPriorityEnum] = Field(None, description="Nova prioridade do TODO")
    status: Optional[TodoStatusEnum] = Field(None, description="Novo status do TODO")
    due_date: Optional[datetime] = Field(None, description="Nova data de vencimento do TODO")


class TodoStatusUpdateRequest(BaseModel):
    """Schema para atualização apenas do status"""
    status: TodoStatusEnum = Field(..., description="Novo status do TODO")


# Schemas de saída (Response)
class TodoResponse(BaseModel):
    """Schema de resposta para TODO"""
    id: UUID = Field(..., description="ID único do TODO")
    title: str = Field(..., description="Título do TODO")
    description: Optional[str] = Field(None, description="Descrição do TODO")
    status: str = Field(..., description="Status atual do TODO")
    priority: str = Field(..., description="Prioridade do TODO")
    due_date: Optional[datetime] = Field(None, description="Data de vencimento do TODO")
    created_at: datetime = Field(..., description="Data de criação do TODO")
    updated_at: datetime = Field(..., description="Data da última atualização do TODO")
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_domain(cls, todo) -> "TodoResponse":
        """Cria um schema de resposta a partir de uma entidade de domínio"""
        return cls(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            priority=todo.priority,
            due_date=todo.due_date,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        )


class TodoListResponse(BaseModel):
    """Schema de resposta para lista de TODOs"""
    todos: list[TodoResponse] = Field(..., description="Lista de TODOs")
    total: int = Field(..., description="Total de TODOs encontrados")
    limit: int = Field(..., description="Limite aplicado na consulta")
    offset: int = Field(..., description="Offset aplicado na consulta")


class TodoStatsResponse(BaseModel):
    """Schema de resposta para estatísticas dos TODOs"""
    total: int = Field(..., description="Total de TODOs")
    pending: int = Field(..., description="TODOs pendentes")
    in_progress: int = Field(..., description="TODOs em progresso")
    completed: int = Field(..., description="TODOs completos")


class ErrorResponse(BaseModel):
    """Schema de resposta para erros"""
    message: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")