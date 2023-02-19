"""Testing redis controllers."""

import pytest

import json
import redis

from tests import DataSource
from tests.conftest import temp_db
from config import config
from data import RedisGraph


@pytest.mark.asyncio
@temp_db
async def test_graph_controller(session):
    """Test redis graph creation"""

    ds = DataSource(session)
    await ds.make_user()

    graph = RedisGraph(name="test")

    response = await ds.client.post(
        "/redis/graph", headers=ds.headers["Test_user"], data=graph.json()
    )
    response = await ds.client.post(
        "/redis/graph", headers=ds.headers["Test_user"], data=graph.json()
    )
    assert response.status_code == 200
