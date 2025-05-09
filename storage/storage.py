"""
Storage class used by Vortex, governs I/O and CRUD for postgres, obsidian, or both.
"""

from Vortex.database.PGRES_tasks import insert_task, get_all_tasks, get_task_by_id


class Storage:
    pass


class PostgresStorage:
    pass


class MarkdownStorage:
    pass
