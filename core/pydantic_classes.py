from pydantic import BaseModel, Field
from enum import Enum
from uuid import uuid4, UUID
from typing import Optional, Any


# Pydantic classes
class Priority(Enum):
    """
    Initialize with either the int as normal OR a list of exclams.
    """

    SOMEDAY = 5
    LOW = 4
    MEDIUM = 3
    HIGH = 2
    CRITICAL = 1

    @classmethod
    def _missing_(cls, value):
        """Handle cases when the value isn't directly in the enum"""
        # If it's a string with exclamation marks
        if isinstance(value, str) and all(char == "!" for char in value):
            # Count the number of exclamation marks
            exclamation_count = len(value)

            # Map the count to priority levels (you can adjust this logic)
            if exclamation_count >= 5:
                return cls.CRITICAL
            elif exclamation_count == 4:
                return cls.HIGH
            elif exclamation_count == 3:
                return cls.MEDIUM
            elif exclamation_count == 2:
                return cls.LOW
            elif exclamation_count == 1:
                return cls.SOMEDAY
        # If we can't handle this value, return None (default behavior)
        return None


class Status(Enum):
    TODO = 1
    INPROGRESS = 2
    BLOCKED = 3
    WAITINGFOR = 4
    DONE = 5


# class Profile -- this is a collection of data about a person, whether it's biographical, a history of correspondence, or the latest task requested by them. Ask questions like "how's my relationship with X?"
class Profile(BaseModel):
    name: str
    # correspondence: Correspondence
    pass


class Document(BaseModel):
    name: str
    path: Optional[str]
    embedding: Any
    embedding_collection: Any


class Task(BaseModel):
    task: str = Field(description="The task, i.e. 'Buy milk at the grocery store'")
    context: Optional[str] = Field(
        description="Optionally more context, whether it be URLs, notes, etc.",
        default="",
    )
    status: Status = Field(description="1-5, from TODO to DONE", default=Status.TODO)
    priority: Priority = Field(
        description="1-5, from CRITICAL to SOMEDAY", default=Priority.MEDIUM
    )
    tags: set = Field(description="All tags associated with this task.", default=set())
    id: UUID = Field(
        description="ID for back-end referencing purposes", default_factory=uuid4
    )


class Project(BaseModel):
    """
    A collection of tasks in a sequence.
    """

    name: str = Field(description="Name of the Project")
    tasks: list[Task] = Field(description="The tasks, in a sequence.")
