If I want todo boxes to be clickable -- likely overengineering but hey.

```python
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings

class TodoItem:
    def __init__(self, text):
        self.text = text
        self.completed = False

todos = [
    TodoItem("Buy groceries"),
    TodoItem("Finish Python project"),
    TodoItem("Call mom")
]

def get_formatted_todos():
    result = []
    for i, todo in enumerate(todos):
        checkbox = "[x]" if todo.completed else "[ ]"
        result.append((f"class:checkbox,todo_{i}", f"{checkbox} {todo.text}\n"))
    return result

def on_click(mouse_event):
    # Get line number from mouse event
    line = mouse_event.position.y
    
    if 0 <= line < len(todos):
        # Toggle completion status
        todos[line].completed = not todos[line].completed
        return True
    return False

# Set up key bindings with mouse support
kb = KeyBindings()

@kb.add('q')
def exit_(event):
    """Exit the application."""
    event.app.exit()

# Create the layout
body = FormattedTextControl(get_formatted_todos)
window = Window(body)
layout = Layout(HSplit([window]))

# Create and run the application
app = Application(
    layout=layout,
    key_bindings=kb,
    mouse_support=True,
    full_screen=True
)

# Register mouse handler
@kb.add('c-space')  # Control+Space
def _(event):
    pass

@kb.add('mouse-down')
def _(event):
    if on_click(event.mouse_event):
        # Refresh the display
        event.app.invalidate()

app.run()
```
