"""
Basic controllers for tasks
"""

from celery import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


from data import get_session
from controllers import auth_decorator, create_response
from celery_worker import small_task, create_task_metadata


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/create_task")
@auth_decorator
async def add_simple_task(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    executes simple task
    """
    task_id = uuid()
    response = small_task.apply_async((), task_id=task_id)

    metadata_task = create_task_metadata(response, task_id)
    await session.close()
    return create_response("Task put on Queue!", 200, metadata_task)
