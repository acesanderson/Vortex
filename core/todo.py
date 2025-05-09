from pathlib import Path
from uuid import uuid4
import re
from Vortex.database.PGRES_tasks import (
    insert_task,
    delete_task,
    create_table,
    delete_table,
    get_all_tasks,
    change_status,
)
from Vortex.core.pydantic_classes import (
    Task,
    Priority,
    Status,
)

from rich.console import Console

dir_path = Path(__file__).parent
todo_path = dir_path / "todo.md"
console = Console()


class Vortex:

    def __init__(self, todo_path: str | Path = todo_path):
        self.todo_path = todo_path

    # Our functions
    def parse_task_creation_syntax(self, input: str) -> Task:
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

    def add_task(self, todo: str):
        """
        Add a todo item to the todo list.
        """
        task = self.parse_task_creation_syntax(todo)
        insert_task(task)
        with open(self.todo_path, "a") as f:
            if task.status == Status.DONE:
                f.write(f"- [x] {task.task}\n")
            else:
                f.write(f"- [ ] {task.task}\n")
            print(f"Added todo: {todo}")

    def remove_todo(self, todo: str):
        """
        Remove a todo item from the todo list.
        """
        with open(self.todo_path, "r") as f:
            todos = f.readlines()
        with open(self.todo_path, "w") as f:
            for line in todos:
                if line.strip("\n") != todo:
                    f.write(line)
        # Postgres CRUD
        delete_task(todo)
        print(f"Removed todo: {todo}")

    def complete_task(self, task: Task):
        """
        Mark a todo item as complete.
        """
        # Markdown CRUD
        with open(self.todo_path, "r") as f:
            lines = f.readlines()
        with open(self.todo_path, "w") as f:
            for line in lines:
                if line.replace("- [ ] ", "").strip("\n") == task.task:
                    f.write(f"- [x] {task.task}\n")
                else:
                    f.write(line)
        # Postgres CRUD
        change_status(task.id, Status.DONE)
        print(f"Completed todo: {task.task}")

    def list_todos(self) -> list[Task]:
        """
        List all todo items in the todo list.
        """
        tasks = get_all_tasks()
        return tasks


if __name__ == "__main__":
    create_table()
    task = Task(task="Get Coursera competitive analysis")
    insert_task(task)
    tasks = get_all_tasks()
    print(tasks)
