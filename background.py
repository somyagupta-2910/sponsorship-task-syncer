from apscheduler.schedulers.asyncio import AsyncIOScheduler
from integrations.salesforce import fetch_tasks as fetch_salesforce_tasks
from integrations.asana import fetch_tasks as fetch_asana_tasks
from integrations.google_calendar import fetch_tasks as fetch_gcal_tasks
from storage import list_sponsors, upsert_tasks

scheduler = AsyncIOScheduler()

async def sync_all_sponsors():
    sponsors = await list_sponsors()
    for sponsor_id in sponsors:
        tasks = []
        tasks.extend(fetch_salesforce_tasks(sponsor_id))
        tasks.extend(fetch_asana_tasks(sponsor_id))
        tasks.extend(fetch_gcal_tasks(sponsor_id))
        await upsert_tasks(tasks)
    print("[ETL] Synced tasks for sponsors:", sponsors)

def start_scheduler():
    scheduler.add_job(sync_all_sponsors, 'interval', minutes=5, id='etl_sync')
    scheduler.start() 