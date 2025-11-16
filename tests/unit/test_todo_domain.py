import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from src.domain.todo import Todo, TodoStatus, TodoPriority


class TestTodo:
    """Testes para a entidade Todo"""
    
    def test_create_todo_with_defaults(self):
        """Testa criação de TODO com valores padrão"""
        todo = Todo(title="Test Task")
        
        assert todo.title == "Test Task"
        assert todo.description is None
        assert todo.status == TodoStatus.PENDING
        assert todo.priority == TodoPriority.MEDIUM
        assert todo.due_date is None
        assert todo.id is not None
        assert todo.created_at is not None
        assert todo.updated_at is not None
    
    def test_create_todo_with_all_fields(self):
        """Testa criação de TODO com todos os campos"""
        todo_id = uuid4()
        due_date = datetime.now() + timedelta(days=7)
        created_at = datetime.now()
        updated_at = datetime.now()
        
        todo = Todo(
            id=todo_id,
            title="Complete Task",
            description="This is a test task",
            priority=TodoPriority.HIGH,
            status=TodoStatus.IN_PROGRESS,
            due_date=due_date,
            created_at=created_at,
            updated_at=updated_at
        )
        
        assert todo.id == todo_id
        assert todo.title == "Complete Task"
        assert todo.description == "This is a test task"
        assert todo.priority == TodoPriority.HIGH
        assert todo.status == TodoStatus.IN_PROGRESS
        assert todo.due_date == due_date
        assert todo.created_at == created_at
        assert todo.updated_at == updated_at
    
    def test_mark_as_completed(self):
        """Testa marcação de TODO como completo"""
        todo = Todo(title="Test Task")
        initial_updated_at = todo.updated_at
        
        todo.mark_as_completed()
        
        assert todo.status == TodoStatus.COMPLETED
        assert todo.updated_at > initial_updated_at
    
    def test_mark_as_in_progress(self):
        """Testa marcação de TODO como em progresso"""
        todo = Todo(title="Test Task")
        initial_updated_at = todo.updated_at
        
        todo.mark_as_in_progress()
        
        assert todo.status == TodoStatus.IN_PROGRESS
        assert todo.updated_at > initial_updated_at
    
    def test_update_title(self):
        """Testa atualização do título"""
        todo = Todo(title="Original Title")
        initial_updated_at = todo.updated_at
        
        todo.update_title("New Title")
        
        assert todo.title == "New Title"
        assert todo.updated_at > initial_updated_at
    
    def test_update_description(self):
        """Testa atualização da descrição"""
        todo = Todo(title="Test Task")
        initial_updated_at = todo.updated_at
        
        todo.update_description("New description")
        
        assert todo.description == "New description"
        assert todo.updated_at > initial_updated_at
    
    def test_update_priority(self):
        """Testa atualização da prioridade"""
        todo = Todo(title="Test Task")
        initial_updated_at = todo.updated_at
        
        todo.update_priority(TodoPriority.HIGH)
        
        assert todo.priority == TodoPriority.HIGH
        assert todo.updated_at > initial_updated_at
    
    def test_update_due_date(self):
        """Testa atualização da data de vencimento"""
        todo = Todo(title="Test Task")
        initial_updated_at = todo.updated_at
        new_due_date = datetime.now() + timedelta(days=5)
        
        todo.update_due_date(new_due_date)
        
        assert todo.due_date == new_due_date
        assert todo.updated_at > initial_updated_at
    
    def test_todo_equality(self):
        """Testa igualdade entre TODOs"""
        todo_id = uuid4()
        todo1 = Todo(id=todo_id, title="Task 1")
        todo2 = Todo(id=todo_id, title="Task 2")
        todo3 = Todo(title="Task 3")
        
        assert todo1 == todo2  # Mesmo ID
        assert todo1 != todo3  # IDs diferentes
    
    def test_todo_hash(self):
        """Testa hash de TODOs"""
        todo_id = uuid4()
        todo1 = Todo(id=todo_id, title="Task 1")
        todo2 = Todo(id=todo_id, title="Task 2")
        
        assert hash(todo1) == hash(todo2)  # Mesmo ID
    
    def test_todo_repr(self):
        """Testa representação string do TODO"""
        todo = Todo(title="Test Task")
        repr_str = repr(todo)
        
        assert "Todo(" in repr_str
        assert f"id={todo.id}" in repr_str
        assert "title='Test Task'" in repr_str
        assert f"status={TodoStatus.PENDING}" in repr_str