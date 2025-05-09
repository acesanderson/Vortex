"""
One facade for Vortex.core. Leverages argparse.
"""

from Vortex.core.todo import *  # type: ignore
from Vortex.display.display import VortexDisplay
from Vortex.obsidian.obsidian import get_today_doc
from rich.console import Console
from Chain import CLI, arg
from pathlib import Path


class VortexCLI(CLI):

    def __init__(
        self, name: str = "VortexCLI", todo_file: str | Path = get_today_doc()
    ):
        super().__init__(name=name)
        self.todo_path = get_today_doc()
        self.console = Console()
        self.display = VortexDisplay(self.console)

    @arg("")
    def arg_insert(self, task):
        """
        Insert a task into the todo list.
        """
        add_task(task)
        self.display.display_tasks()

    @arg("-l")
    def arg_list(self):
        """
        List all tasks in the todo list.
        """
        self.display.display_tasks()

    @arg("-c")
    def arg_context(self, context: str):
        """
        Set the context for the todo list.
        """
        pass


def main():
    cli = VortexCLI()
    cli.run()


if __name__ == "__main__":
    main()
