"""Tests for util functions."""
import json

import pytest
import redis

from tests import DataSource
from tests.conftest import temp_db
from config import config


@pytest.mark.asyncio
@temp_db("async_session")
async def test_small_task(session):
    """Test authenthication."""

    ds = DataSource(session)
    await ds.make_user()

    response = await ds.client.post(
        "/tasks/create_task", headers=ds.headers["Test_user"]
    )
    assert response.status_code == 200
    task_metadata = json.loads(response.text)
    task_id = task_metadata["item"]["task_id"]
    redis_connection = redis.from_url(config.redis_url)
    while True:
        value = redis_connection.get("celery-task-meta-" + task_id)
        if not value:
            continue
        value = json.loads(value)["result"]
        break

    assert value == {"small_task": 2}
