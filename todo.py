from pathlib import Path
from pydantic import BaseModel, Field
import argparse, sys
from typing import Optional
from enum import Enum
from rich.console import Console

dir_path = Path(__file__).parent
todo_path = dir_path / "todo.md"
console = Console()


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


class Task(BaseModel):
    task: str = Field(description="The task, i.e. 'Buy milk at the grocery store'")
    context: Optional[str] = Field(
        description="Optionally more context, whether it be URLs, notes, etc."
    )
    status: Status = Field(description="1-5, from TODO to DONE", default=Status.TODO)
    priority: Priority = Field(
        description="1-5, from CRITICAL to SOMEDAY", default=Priority.MEDIUM
    )
    tags: set = Field(description="All tags associated with this task.", default=set())


class Project(BaseModel):
    """
    A collection of tasks in a sequence.
    """

    name: str = Field(description="Name of the Project")
    tasks: list[Task] = Field(description="The tasks, in a sequence.")


def add_todo(todo: str):
    """
    Add a todo item to the todo list.
    """
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


def main():
    parser = argparse.ArgumentParser(description="Add a todo item to the todo list.")
    # We want to be able to just type whatever we want without quotes in bash, hence nargs = *.
    parser.add_argument("todo", type=str, nargs="*", help="The todo item to add.")
    parser.add_argument(
        "-l", "--list", action="store_true", help="List all todo items."
    )
    parser.add_argument("-c", "--clear", action="store_true", help="Clear the todos.")
    args = parser.parse_args()
    if args.clear:
        if todo_path.exists():
            todo_path.unlink()
        todo_path.touch()
        print("To dos deleted.")
        sys.exit()
    if args.list:
        todos = list_todos()
        if todos:
            print("Todo list:")
            for todo in todos:
                print(todo)
        else:
            print("No todos found.")
    else:
        if args.todo:
            # We want to be able to just type whatever we want without quotes in bash.
            todo = " ".join(args.todo)
            add_todo(todo)
        todos = list_todos()
        if todos:
            print("Todo list:")
            for todo in todos:
                print(todo)
        else:
            print("No todos found.")


if __name__ == "__main__":
    main()
