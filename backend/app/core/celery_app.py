from celery import Celery
from app.core.config import settings

celery_app = Celery("octa")

celery_app.conf.update(
    broker_url=settings.redis_url,
    result_backend=settings.redis_url,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    include=["app.tasks.geospatial_tasks"]
) 