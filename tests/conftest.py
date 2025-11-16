import pytest
import asyncio
from typing import Generator

# Configuração para testes assíncronos
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Cria um loop de eventos para testes assíncronos"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_todo_data():
    """Dados de exemplo para testes"""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "medium",
        "status": "pending"
    }