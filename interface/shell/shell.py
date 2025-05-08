from Chain import Chat, Model
from Vortex.core.todo import *  # type: ignore


class VortexChat(Chat):

    def command_add(self, task: str):
        """
        Add a task to the todo list
        """
        add_todo(task)
        self.command_list()

    def command_list(self):
        """
        List all tasks in the todo list
        """
        todos = list_todos()
        for todo in todos:
            print(todo)

    def command_remove(self, task: str):
        """
        Remove a task from the todo list
        """
        remove_todo(task)
        self.command_list()

    def command_complete(self, task: str):
        """
        Mark a task as complete
        """
        complete_todo(task)
        self.command_list()


if __name__ == "__main__":
    chat = VortexChat(model=Model("gpt"))
    chat.chat()
