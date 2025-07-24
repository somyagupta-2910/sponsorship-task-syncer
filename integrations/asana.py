from models import Task
from datetime import datetime, timedelta

def fetch_tasks(sponsor_id: str):
    return [
        Task(
            id="asana-1",
            sponsor_id=sponsor_id,
            source="Asana",
            name="Post campaign assets",
            due_date=datetime.now() + timedelta(days=2),
            status="pending"
        ),
        Task(
            id="asana-2",
            sponsor_id=sponsor_id,
            source="Asana",
            name="Review creative brief",
            due_date=datetime.now() + timedelta(days=4),
            status="completed"
        ),
    ] 