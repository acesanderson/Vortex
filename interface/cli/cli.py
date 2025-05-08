"""
One facade for Vortex.core. Leverages argparse.
"""

from Vortex.core.todo import *  # type: ignore
from Vortex.database.PGRES_tasks import insert_task, get_all_tasks
from Vortex.display.display import VortexDisplay
from Vortex.obsidian.obsidian import get_today_doc
import argparse, sys
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table


def VortexCLI():

    def __init__(self):
        self.todo_path = get_today_doc()
        self.todos = list_todos()

    pass


def main():
    console = Console()
    display = VortexDisplay(console)
    parser = argparse.ArgumentParser(description="Add a todo item to the todo list.")
    # We want to be able to just type whatever we want without quotes in bash, hence nargs = *.
    parser.add_argument("todo", type=str, nargs="*", help="The todo item to add.")
    parser.add_argument(
        "-c", "--context", type=str, help="The context for the todo item."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List all todo items."
    )
    parser.add_argument("-w", "--wipe", action="store_true", help="Clear the todos.")
    args = parser.parse_args()
    if args.wipe:
        if todo_path.exists():
            todo_path.unlink()
        todo_path.touch()
        print("To dos deleted.")
        sys.exit()
    if args.list:
        display.display_tasks()
    else:
        if args.todo:
            # We want to be able to just type whatever we want without quotes in bash.
            todo = " ".join(args.todo)
            insert_task(Task(task=todo))
        display.display_tasks()


if __name__ == "__main__":
    main()
