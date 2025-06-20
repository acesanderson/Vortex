"""
One facade for Vortex.core. Leverages argparse.
"""

from Vortex.core.todo import Vortex

# from Vortex.obsidian.obsidian import get_today_doc
from rich.console import Console
from Chain import CLI, arg
from pathlib import Path

dir_path = Path(__file__).parent


class VortexCLI(CLI):

    def __init__(
        self,
        todo_file: str | Path,
        name: str = "VortexCLI",
    ):
        super().__init__(name=name)
        self.todo_path = todo_file
        self.console = Console()
        self.vortex = Vortex(self.todo_path)

    def view_todos(self):
        """
        Display function.
        """
        tasks = self.vortex.list_todos()
        for index, task in enumerate(tasks):
            self.console.print(
                f"[bold white] - [ ] [/bold white][bold yellow]{index+1}[/bold yellow] [green]{task.task}[/green] - {task.status} - {task.priority}"
            )

    @arg("")
    def arg_insert(self, task):
        """
        Insert a task into the todo list.
        """
        self.vortex.add_task(task)
        self.view_todos()

    @arg("-l")
    def arg_list(self):
        """
        List all tasks in the todo list.
        """
        self.view_todos()

    @arg("-c")
    def arg_context(self, context: str):
        """
        Set the context for the todo list.
        """
        pass

    def _default(self):
        """
        Default function.
        """
        self.view_todos()


def main():
    todo_path = dir_path / "todo.md"
    cli = VortexCLI(todo_file=todo_path)
    cli.run()


if __name__ == "__main__":
    main()
