"""Celery application setup for the tw project."""

from __future__ import annotations

import os
from celery import Celery


def _redis_url(db_default: int) -> str:
    host = os.getenv("REDIS_HOST", "redis")
    port = os.getenv("REDIS_PORT", "6379")
    password = os.getenv("REDIS_PASSWORD")
    db = os.getenv("REDIS_DB", str(db_default))

    auth = f":{password}@" if password else ""
    return f"redis://{auth}{host}:{port}/{db}"


broker_url = os.getenv("CELERY_BROKER_URL", _redis_url(db_default=0))
result_backend = os.getenv("CELERY_RESULT_BACKEND", _redis_url(db_default=1))

celery_app = Celery("tw", broker=broker_url, backend=result_backend)

celery_app.conf.update(
    task_default_queue=os.getenv("CELERY_DEFAULT_QUEUE", "default"),
    task_track_started=True,
    task_time_limit=int(os.getenv("CELERY_TASK_TIME_LIMIT", "300")),
    worker_max_tasks_per_child=int(os.getenv("CELERY_MAX_TASKS_PER_CHILD", "100")),
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone=os.getenv("CELERY_TIMEZONE", "UTC"),
    enable_utc=True,
)


def _modules() -> list[str]:
    """Return packages that contain celery tasks."""

    modules: list[str] = ["tw"]
    extra = os.getenv("CELERY_TASK_PACKAGES")
    if extra:
        modules.extend([item.strip() for item in extra.split(",") if item.strip()])
    return modules


celery_app.set_default()
celery_app.autodiscover_tasks(_modules, related_name="tasks")


__all__ = ["celery_app"]

