"""
CRUD functions for course tools.

We will use this database for:
- storing specific data keyed to courses like
    - tools used in each course
- this will be ideal on local network for parallelized tasks
"""

from Vortex.database.PGRES_connection import get_db_connection
import psycopg2
from pathlib import Path
from rich.console import Console
from typing import Optional
from uuid import UUID
from Vortex.core.pydantic_classes import (
    Task,
)

console = Console()
dir_path = Path(__file__).parent


# Create table
def create_table():
    """
    Create a table in the database.
    Table name = tools
    Two columns:
    - course_admin_id (int)
    - tools_counter (jsonb) - stores a Python Counter object
    """
    query = "CREATE TABLE IF NOT EXISTS tasks (task VARCHAR(255) UNIQUE, context TEXT, status INT, priority INT, tags TEXT[], id UUID PRIMARY KEY);"
    # Enable UUID extension if not already enabled
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        cursor.execute(query)
        conn.commit()
        console.print("[cyan]Tasks table created successfully.[/cyan]")


def insert_task(task: Task):
    """
    Insert or update a Task object.

    Args:
        task: the Task object
    """
    # Convert Task object to dict
    task_dict = task.model_dump()

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (task, context, status, priority, tags, id) VALUES (%s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (id) DO NOTHING;",
                (
                    task_dict["task"],
                    task_dict["context"],
                    task_dict["status"].value,
                    task_dict["priority"].value,
                    list(task_dict["tags"]),
                    task_dict["id"],
                ),
            )
            conn.commit()
            console.print(f"[green]Task '{task.task}' saved successfully.[/green]")
    except psycopg2.errors.UniqueViolation:
        console.print(f"[green]Task '{task.task}' already in database.[/green]")
        pass


def get_task_by_id(id: str) -> Optional[Task]:
    """
    Get the tools Counter for a specific course.

    Args:
        course_admin_id (int): The course identifier

    Returns:
        Counter or None: Counter object with tool frequencies, None if not found
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT task, context, status, priority, tags, id FROM tasks WHERE id = %s",
            (id,),
        )
        result = cursor.fetchone()

        if result is None:
            return None

        # Convert result to Task object
        task = Task(
            task=result[0],
            context=result[1],
            status=result[2],
            priority=result[3],
            tags=set(result[4]),
            id=UUID(result[5]),
        )
        return task


def get_all_tasks() -> list[Task]:
    """
    Get all tasks from the database.

    Returns:
        list: List of Task objects
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task, context, status, priority, tags, id FROM tasks")
        results = cursor.fetchall()
        tasks = []
        for row in results:
            task = Task(
                task=row[0],
                context=row[1],
                status=row[2],
                priority=row[3],
                tags=set(row[4]),
                id=row[5],
            )
            tasks.append(task)
    return tasks


def get_task_dict() -> dict[UUID, str]:
    """
    Get a dictionary with key as task ID and value as task name.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, task FROM tasks")
        results = cursor.fetchall()
        return {UUID(row[0]): row[1] for row in results}


def clear_table():
    """
    Clear all data from the tools table.
    Only use this manually.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        console.print("[yellow]Tasks table cleared successfully.[/yellow]")


def delete_table():
    """
    Delete the tools table entirely.
    Only use this manually.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS tasks")
        conn.commit()
        console.print("[yellow]Tasks table deleted successfully.[/yellow]")
