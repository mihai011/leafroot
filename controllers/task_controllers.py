"""
Basic controllers for tasks
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from data import get_session
from controllers import auth_decorator, create_response
from celery_worker import small_task


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
    small_task.delay()
    await session.close()
    return create_response("Task put on Queue!", 200, True)
