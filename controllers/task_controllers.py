"""Basic controllers for tasks."""

from celery import uuid
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser
from celery_worker import small_task, create_task_metadata
from data import TaskResponseItem


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/create_task", response_model=TaskResponseItem)
async def add_simple_task(_: CurrentUser) -> ORJSONResponse:
    """Execute simple task."""
    task_id = uuid()
    response = small_task.apply_async((), task_id=task_id)

    metadata_task = create_task_metadata(response, task_id)
    metadata_task
    return create_response(
        message="Task put on Queue!",
        status=status.HTTP_200_OK,
        response_model=TaskResponseItem,
        item=metadata_task,
    )
