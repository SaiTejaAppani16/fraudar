from celery import Celery
from backend.config import REDIS_URL

celery_app = Celery(
    "fraudar",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["backend.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600  # Results expire after 1 hour
)