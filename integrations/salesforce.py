from models import Task
from datetime import datetime, timedelta

def fetch_tasks(sponsor_id: str):
    return [
        Task(
            id="sf-1",
            sponsor_id=sponsor_id,
            source="Salesforce",
            name="Finalize contract",
            due_date=datetime.now() + timedelta(days=3),
            status="pending"
        ),
        Task(
            id="sf-2",
            sponsor_id=sponsor_id,
            source="Salesforce",
            name="Upload logo",
            due_date=datetime.now() + timedelta(days=5),
            status="pending"
        ),
    ] 