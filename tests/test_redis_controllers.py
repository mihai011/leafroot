"""Testing redis controllers."""

import pytest

import json
import redis

from tests import DataSource
from tests.conftest import temp_db
from config import config
from data import RedisGraph, RedisNode, RedisEdge
from data import get_redis_connection


@pytest.mark.asyncio
@temp_db
async def test_graph_controller(session):
    """Test redis graph creation"""

    ds = DataSource(session)
    await ds.make_user()
    redis_client = next(get_redis_connection())

    graph = RedisGraph(name="test")

    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph.json(),
    )
    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph.json(),
    )
    assert redis_client.exists("test")

    response = await ds.client.get(
        "/redis-graph/graph/test", headers=ds.headers["Test_user"]
    )

    graph_data = json.loads(response.content)["item"]
    assert len(graph_data["nodes"]) == 1

    graph = redis_client.graph("test")
    graph.delete()


@pytest.mark.asyncio
@temp_db
async def test_graph_add_nodes(session):
    """Test node adding to graph."""

    graph_name = "Locations2"
    ds = DataSource(session)
    await ds.make_user()
    redis_client = next(get_redis_connection())

    graph = RedisGraph(name=graph_name)
    node = RedisNode(
        graph=graph_name, label="Bucharest", properties={"test": "property"}
    )

    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph.json(),
    )
    assert response.status_code == 200
    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == 1

    response = await ds.client.post(
        "/redis-graph/node", headers=ds.headers["Test_user"], data=node.json()
    )
    assert response.status_code == 200
    graph = json.loads(response.content)["item"]

    response = await ds.client.get(
        f"/redis-graph/graph/{graph_name}", headers=ds.headers["Test_user"]
    )

    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == 2

    graph = redis_client.graph(graph_name)
    graph.delete()


@pytest.mark.asyncio
@temp_db
async def test_graph_add_edge(session):
    """Test add edge to graph."""

    ds = DataSource(session)
    await ds.make_user()
    redis_client = next(get_redis_connection())

    graph = RedisGraph(name="Locations")

    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph.json(),
    )
    assert response.status_code == 200

    node_1 = RedisNode(
        graph="Locations", label="Bucharest", properties={"area": 10000}
    )
    node_2 = RedisNode(
        graph="Locations", label="Craiova", properties={"test": 100}
    )

    response = await ds.client.post(
        "/redis-graph/node",
        headers=ds.headers["Test_user"],
        data=node_1.json(),
    )

    src = json.loads(response.content)["item"]["alias"]

    response = await ds.client.post(
        "/redis-graph/node",
        headers=ds.headers["Test_user"],
        data=node_2.json(),
    )

    dst = json.loads(response.content)["item"]["alias"]

    edge = RedisEdge(
        graph="Locations", source=src, destination=dst, relation="relation"
    )

    response = await ds.client.post(
        "/redis-graph/edge", headers=ds.headers["Test_user"], data=edge.json()
    )

    assert response.status_code == 200

    response = await ds.client.get(
        "/redis-graph/graph/Locations", headers=ds.headers["Test_user"]
    )

    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == 3
    assert graph["edges"] == 1

    graph = redis_client.graph("Locations")
    graph.delete()
