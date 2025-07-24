from fastapi import FastAPI, Depends, Query, Body, HTTPException
from models import Task
from auth import get_api_key
from typing import List, Optional
from integrations.salesforce import fetch_tasks as fetch_salesforce_tasks
from integrations.asana import fetch_tasks as fetch_asana_tasks
from integrations.google_calendar import fetch_tasks as fetch_gcal_tasks
from storage import (
    database, upsert_tasks, fetch_tasks_by_sponsor, update_task_status,
    add_sponsor, list_sponsors, remove_sponsor
)
from datetime import datetime
from background import start_scheduler

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    start_scheduler()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/sync-tasks", response_model=List[Task])
async def sync_tasks(sponsor_id: str, api_key: str = Depends(get_api_key)):
    tasks = []
    tasks.extend(fetch_salesforce_tasks(sponsor_id))
    tasks.extend(fetch_asana_tasks(sponsor_id))
    tasks.extend(fetch_gcal_tasks(sponsor_id))
    await upsert_tasks(tasks)
    return tasks

@app.post("/sponsors")
async def post_sponsor(
    sponsor_id: str = Body(..., embed=True, description="Sponsor ID to add"),
    api_key: str = Depends(get_api_key)
):
    await add_sponsor(sponsor_id)
    return {"sponsor_id": sponsor_id, "message": "Sponsor added"}

@app.get("/sponsors")
async def get_sponsors(api_key: str = Depends(get_api_key)):
    sponsors = await list_sponsors()
    return {"sponsors": sponsors}

@app.delete("/sponsors/{sponsor_id}")
async def delete_sponsor(sponsor_id: str, api_key: str = Depends(get_api_key)):
    await remove_sponsor(sponsor_id)
    return {"sponsor_id": sponsor_id, "message": "Sponsor removed"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks(
    sponsor_id: str = Query(..., description="Sponsor ID"),
    status: Optional[str] = Query(None, description="Task status"),
    source: Optional[str] = Query(None, description="Source system"),
    due_before: Optional[datetime] = Query(None, description="Due before (ISO format)"),
    due_after: Optional[datetime] = Query(None, description="Due after (ISO format)"),
    api_key: str = Depends(get_api_key)
):
    return await fetch_tasks_by_sponsor(
        sponsor_id=sponsor_id,
        status=status,
        source=source,
        due_before=due_before,
        due_after=due_after
    )

@app.patch("/tasks/{task_id}")
async def patch_task_status(
    task_id: str,
    status: str = Body(..., embed=True, description="New status for the task"),
    api_key: str = Depends(get_api_key)
):
    updated = await update_task_status(task_id, status)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": status, "message": "Task status updated"} 