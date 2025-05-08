"""
One facade for Vortex.core. Leverages argparse.
"""

from Vortex.core.todo import *  # type: ignore
import argparse, sys


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
