from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "ip_tracker_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "refresh-saved-ips-every-12-hours": {
            "task": "app.workers.tasks.refresh_all_ips_task",
            "schedule": 60 * 60 * 12,
        }
    },
)