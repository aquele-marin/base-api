from enum import Enum


class TodoStatusEnum(str, Enum):
    """Enum for Todo status values used in API schemas"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriorityEnum(str, Enum):
    """Enum for Todo priority values used in API schemas"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
