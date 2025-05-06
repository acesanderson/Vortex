from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, Any
from enum import Enum
from uuid import uuid4, UUID
import re

from rich.console import Console

dir_path = Path(__file__).parent
todo_path = dir_path / "todo.md"
console = Console()


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


# Our functions
def parse_task_creation_syntax(input: str) -> Task:
    """
    We have a special syntax for creating tasks.
    !+: priority
    -s: status (TODO, INPROGRESS, BLOCKED, WAITINGFOR, DONE)
    #: tag(s)
    +: project(s)

    TBD: project handling (this is where we leverage postgres)
    """
    # Capture our different syntax items
    ## These should have 0-1 hits
    priority_match = re.search("( !+)", input)
    status_match = re.search("( -s [^ ]+)", input)
    ## These should have 0-infinity hits
    tag_match = re.search("( # [^ ]+)", input)
    project_match = re.search("( \\+ [^ ]+)", input)
    # Parse any hits
    ## Priority
    if priority_match:
        priority = priority_match.group()
        input = input.replace(priority, "")
        priority = priority.replace(" ", "")
        priority = Priority(priority)
    else:
        priority = Priority.MEDIUM
    ## Status
    if status_match:
        status = status_match.group()
        input = input.replace(status, "")
        status = status.replace(" ", "")
        status = Status(status)
    else:
        status = Status.TODO
    ## Tags - there can be multiple tags
    tags = []
    if tag_match:
        tags = tag_match.group()
        input = input.replace(tags, "")
        tags = tags.replace(" ", "")
        tags = tags.split("#")
        tags = [tag for tag in tags if tag != ""]
        tags = set(tags)
    else:
        tags = set()
    ## Projects - there can be multiple projects; this is a TBD
    projects = []
    if project_match:
        projects = project_match.group()
        input = input.replace(projects, "")
        projects = projects.replace(" ", "")
        projects = projects.split("+")
        projects = [project for project in projects if project != ""]
    # Build our Task
    task = Task(
        task=input,
        context="",
        status=status,
        priority=priority,
        tags=tags,
        id=uuid4(),
    )
    return task


def add_todo(todo: str):
    """
    Add a todo item to the todo list.
    """
    task = parse_task_creation_syntax(todo)
    _ = task  # Eventually we will save this to a database
    with open(todo_path, "a") as f:
        f.write(f"- [ ] {todo}\n")
    print(f"Added todo: {todo}")


def list_todos() -> list[str]:
    """
    List all todo items in the todo list.
    """
    if not todo_path.exists():
        todo_path.touch()
    with open(todo_path, "r") as f:
        todos = f.readlines()
    return [todo.strip() for todo in todos]


if __name__ == "__main__":
    test = "go to work !!!"
    parse_task_creation_syntax(test)
