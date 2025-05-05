from pathlib import Path
import argparse

todo_path = Path("/Users/bianders/MorphyMobile/todo.md")


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
    with open(todo_path, "r") as f:
        todos = f.readlines()
    return [todo.strip() for todo in todos]


def main():
    parser = argparse.ArgumentParser(description="Add a todo item to the todo list.")
    parser.add_argument("todo", type=str, nargs="?", help="The todo item to add.")
    parser.add_argument(
        "-l", "--list", action="store_true", help="List all todo items."
    )
    args = parser.parse_args()
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
            add_todo(args.todo)
        todos = list_todos()
        if todos:
            print("Todo list:")
            for todo in todos:
                print(todo)
        else:
            print("No todos found.")


if __name__ == "__main__":
    main()
