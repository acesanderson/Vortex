"""
Both CLI and shell share similar formatting. We'll define it here.
This Display class converts the Core logic to rich-formatted output.
"""

from rich.console import Console
from Vortex.core.todo import list_todos


class VortexDisplay:

    def __init__(self, console: Console):
        self.console = console

    def display_tasks(self):
        tasks = list_todos()
        for index, task in enumerate(tasks):
            self.console.print(
                f"[bold white] - [ ] [/bold white][bold yellow]{index+1}[/bold yellow] [green]{task.task}[/green] - {task.status} - {task.priority}"
            )
