from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.infra import Base


class TodoStatus(Base):
    __tablename__ = "todo_statuses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relationship to Todo
    todos = relationship("Todo", back_populates="status_ref")
    
    def __repr__(self):
        return f"<TodoStatus(id={self.id}, value='{self.value}')>"
    
    def __eq__(self, other):
        """Allow comparison with string values"""
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, TodoStatus):
            return self.value == other.value
        return False