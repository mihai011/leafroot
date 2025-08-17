"""Module for celery task queue related functionality."""

from uuid import UUID

from celery import Celery
from celery.result import AsyncResult

from config import config

app = Celery(__name__, backend=config.redis_url, broker=config.celery_broker_url)


def create_task_metadata(result: AsyncResult, task_id: UUID) -> dict:
    """Generates metadata about the task."""
    metadata = result._get_task_meta()  # noqa: SLF001
    metadata["task_id"] = task_id

    return metadata


@app.task
def small_task() -> dict:
    """Small tasks for celery."""
    return {"small_task": 2}
