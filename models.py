from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    id: str
    sponsor_id: str
    source: str  # e.g., 'Salesforce', 'Asana', 'Google Calendar'
    name: str
    due_date: Optional[datetime] = None
    status: str  # e.g., 'pending', 'completed', etc. 