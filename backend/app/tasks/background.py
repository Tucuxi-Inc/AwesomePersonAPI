"""Background tasks for Celery."""

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True)
def example_task(self, message: str) -> dict:
    """Example background task."""
    return {"status": "completed", "message": message}
