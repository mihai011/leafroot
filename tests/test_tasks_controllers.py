"""
tests for util functions
"""

import json
import aioredis

from tests import DataSource
from tests.conftest import temp_db
from config import CELERY_RESULT_BACKEND


@temp_db
async def test_small_task(session):
    """
    test authenthication
    """

    ds = DataSource(session)
    await ds.make_user()

    response = await ds.client.post(
        "/tasks/create_task", headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200
    task_metadata = json.loads(response.text)
    task_id = task_metadata["item"]["task_id"]
    redis = aioredis.from_url(CELERY_RESULT_BACKEND)
    value = await redis.get("celery-task-meta-" + task_id)
    value = json.loads(value)["result"]
    assert value == {"small_task": 1}
