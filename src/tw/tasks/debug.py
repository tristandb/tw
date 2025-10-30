"""Debug tasks for system health checks."""

from tw.celery_app import celery_app


@celery_app.task(name="tw.debug.ping")
def ping() -> str:
    """Simple heartbeat task used for smoke testing the worker."""
    return "pong"