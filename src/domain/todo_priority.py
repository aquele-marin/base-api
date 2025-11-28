from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.infra import Base


class TodoPriority(Base):
    __tablename__ = "todo_priorities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(50), unique=True, nullable=False, index=True)
    
    todos = relationship("Todo", back_populates="priority_ref")
    
    def __repr__(self):
        return f"<TodoPriority(id={self.id}, value='{self.value}')>"
    
    def __eq__(self, other):
        """Allow comparison with string values"""
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, TodoPriority):
            return self.value == other.value
        return False