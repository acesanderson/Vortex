from pathlib import Path
from uuid import uuid4
import re
from Vortex.database.PGRES_tasks import (
    insert_task,
    create_table,
    get_task_by_id,
    get_all_tasks,
)
from Vortex.core.pydantic_classes import (
    Task,
    Project,
    Priority,
    Status,
    Document,
    Profile,
)

from rich.console import Console

dir_path = Path(__file__).parent
todo_path = dir_path / "todo.md"
console = Console()


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


def remove_todo(todo: str):
    """
    Remove a todo item from the todo list.
    """
    with open(todo_path, "r") as f:
        todos = f.readlines()
    with open(todo_path, "w") as f:
        for line in todos:
            if line.strip("\n") != todo:
                f.write(line)
    print(f"Removed todo: {todo}")


def complete_todo(todo: str):
    """
    Mark a todo item as complete.
    """
    with open(todo_path, "r") as f:
        todos = f.readlines()
    with open(todo_path, "w") as f:
        for line in todos:
            if line.strip("\n") == todo:
                f.write(f"- [x] {todo}\n")
            else:
                f.write(line)
    print(f"Completed todo: {todo}")


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
    create_table()
    task = Task(task="Get Coursera competitive analysis")
    insert_task(task)
    tasks = get_all_tasks()
    print(tasks)
