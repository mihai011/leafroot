"""
Module for celery task queue related functionality
"""

from uuid import UUID
from celery import Celery
from celery.result import AsyncResult
from config import CELERY_RESULT_BACKEND, CELERY_BROKER_URL


app = Celery(__name__, backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)


def create_task_metadata(result: AsyncResult, task_id: UUID):
    """
    Generates metadata about the task
    """

    metadata = result._get_task_meta()
    metadata["task_id"] = task_id

    return metadata


@app.task
def small_task():

    return {"small_task": 1}
