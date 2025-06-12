import json
import os
from datetime import datetime

TODO_FILE = "todos.json"

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, 'r') as f:
        return json.load(f)

def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def add_todo(task, due_date=None):
    todos = load_todos()
    todos.append({
        "id": len(todos) + 1,
        "task": task,
        "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
        "completed": False
    })
    save_todos(todos)

def remove_todo(todo_id):
    todos = load_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)

def update_todo(todo_id, **kwargs):
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo.update(kwargs)
    save_todos(todos)
