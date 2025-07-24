from models import Task
from datetime import datetime, timedelta

def fetch_tasks(sponsor_id: str):
    return [
        Task(
            id="gcal-1",
            sponsor_id=sponsor_id,
            source="Google Calendar",
            name="Activation deadline",
            due_date=datetime.now() + timedelta(days=1),
            status="pending"
        ),
        Task(
            id="gcal-2",
            sponsor_id=sponsor_id,
            source="Google Calendar",
            name="Post-event report",
            due_date=datetime.now() + timedelta(days=7),
            status="pending"
        ),
    ] 