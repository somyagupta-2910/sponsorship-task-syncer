import sqlalchemy
from databases import Database
from models import Task
from typing import List, Optional
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./tasks.db"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

tasks_table = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("sponsor_id", sqlalchemy.String, index=True),
    sqlalchemy.Column("source", sqlalchemy.String),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("due_date", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String),
)

sponsors_table = sqlalchemy.Table(
    "sponsors",
    metadata,
    sqlalchemy.Column("sponsor_id", sqlalchemy.String, primary_key=True),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL.replace("+aiosqlite", ""), connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

async def upsert_tasks(tasks: List[Task]):
    for task in tasks:
        query = """
        INSERT INTO tasks (id, sponsor_id, source, name, due_date, status)
        VALUES (:id, :sponsor_id, :source, :name, :due_date, :status)
        ON CONFLICT(id) DO UPDATE SET
            sponsor_id=excluded.sponsor_id,
            source=excluded.source,
            name=excluded.name,
            due_date=excluded.due_date,
            status=excluded.status
        """
        values = task.dict()
        await database.execute(query=query, values=values)

async def fetch_tasks_by_sponsor(
    sponsor_id: str,
    status: Optional[str] = None,
    source: Optional[str] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None
) -> List[Task]:
    query = tasks_table.select().where(tasks_table.c.sponsor_id == sponsor_id)
    if status:
        query = query.where(tasks_table.c.status == status)
    if source:
        query = query.where(tasks_table.c.source == source)
    if due_before:
        query = query.where(tasks_table.c.due_date <= due_before)
    if due_after:
        query = query.where(tasks_table.c.due_date >= due_after)
    rows = await database.fetch_all(query)
    return [Task(**dict(row)) for row in rows]

async def update_task_status(task_id: str, status: str) -> bool:
    query = """
    UPDATE tasks
    SET status = :status
    WHERE id = :task_id
    """
    result = await database.execute(query=query, values={"status": status, "task_id": task_id})
    return result is not None

async def add_sponsor(sponsor_id: str):
    query = sponsors_table.insert().values(sponsor_id=sponsor_id)
    try:
        await database.execute(query)
    except Exception:
        pass  # Ignore if already exists

async def list_sponsors() -> list:
    query = sponsors_table.select()
    rows = await database.fetch_all(query)
    return [row["sponsor_id"] for row in rows]

async def remove_sponsor(sponsor_id: str):
    query = sponsors_table.delete().where(sponsors_table.c.sponsor_id == sponsor_id)
    await database.execute(query) 