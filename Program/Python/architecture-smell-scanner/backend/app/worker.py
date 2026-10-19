from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "smell_scanner",
    broker=settings.CELERY_BROKER_URL or settings.REDIS_URL,
    backend=settings.CELERY_RESULT_BACKEND or settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=600,  # 10 minutes max per scan
)


@celery_app.task(name="run_scan")
def run_scan(scan_id: int):
    """Celery task to run a code scan asynchronously"""
    from app.core.database import async_session_maker
    from app.services.scan_service import ScanService
    import asyncio

    async def _run():
        async with async_session_maker() as db:
            service = ScanService(db)
            await service.start_scan(scan_id)

    asyncio.run(_run())


@celery_app.task(name="cleanup_old_snapshots")
def cleanup_old_snapshots():
    """Celery task to cleanup old code snapshots"""
    import os
    from datetime import datetime, timedelta
    
    storage_path = settings.STORAGE_PATH
    if not os.path.exists(storage_path):
        return
    
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    
    for project_dir in os.listdir(storage_path):
        project_path = os.path.join(storage_path, project_dir)
        if not os.path.isdir(project_path):
            continue
        
        for filename in os.listdir(project_path):
            file_path = os.path.join(project_path, filename)
            if os.path.isfile(file_path):
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff_date:
                    os.remove(file_path)