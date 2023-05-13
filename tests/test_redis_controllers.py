"""Testing redis controllers."""

import json
import random

from fastapi import status
import pytest

from tests import DataSource
from data import RedisGraph, RedisNode, RedisEdge, RedisGraphQuery
from utils import random_string


@pytest.mark.asyncio
async def test_graph_controller(async_session):
    """Test redis graph creation."""

    ds = DataSource(async_session)
    await ds.make_user()
    graph_name = "test"

    graph = RedisGraph(name=graph_name)

    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        f"/redis-graph/graph/{graph_name}", headers=ds.headers["Test_user"]
    )
    graph_data = json.loads(response.content)["item"]
    assert len(graph_data["nodes"]) == 1

    response = await ds.client.post(
        "/redis-graph/graph/flush",
        headers=ds.headers["Test_user"],
        data=graph.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.delete(
        f"/redis-graph/graph/{graph_name}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_graph_add_nodes(async_session):
    """Test node adding to graph."""

    graph_name = "Locations2"
    ds = DataSource(async_session)
    await ds.make_user()

    graph_pyd = RedisGraph(name=graph_name)
    node = RedisNode(
        graph=graph_name, label="Bucharest", properties={"test": "property"}
    )

    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph_pyd.json(),
    )
    assert response.status_code == status.HTTP_200_OK
    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == 1

    response = await ds.client.post(
        "/redis-graph/node", headers=ds.headers["Test_user"], data=node.json()
    )
    assert response.status_code == status.HTTP_200_OK
    graph = json.loads(response.content)["item"]

    response = await ds.client.get(
        f"/redis-graph/graph/{graph_name}", headers=ds.headers["Test_user"]
    )

    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == 2

    response = await ds.client.post(
        "/redis-graph/graph/flush",
        headers=ds.headers["Test_user"],
        data=graph_pyd.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.delete(
        f"/redis-graph/graph/{graph_name}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_graph_add_edge(async_session):
    """Test add edge to graph."""

    ds = DataSource(async_session)
    await ds.make_user()
    graph_name = "Locations"

    graph_pyd = RedisGraph(name=graph_name)

    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph_pyd.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    node_1 = RedisNode(
        graph=graph_name, label="Bucharest", properties={"area": 10000}
    )
    node_2 = RedisNode(
        graph=graph_name, label="Craiova", properties={"test": 100}
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
        graph=graph_name, source=src, destination=dst, relation="relation"
    )

    response = await ds.client.post(
        "/redis-graph/edge", headers=ds.headers["Test_user"], data=edge.json()
    )

    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        f"/redis-graph/graph/{graph_name}", headers=ds.headers["Test_user"]
    )

    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == 3
    assert graph["edges"] == 1

    response = await ds.client.post(
        "/redis-graph/graph/flush",
        headers=ds.headers["Test_user"],
        data=graph_pyd.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    response = await ds.client.delete(
        f"/redis-graph/graph/{graph_name}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_graph_redis(async_session):
    """Test redis graph."""
    ds = DataSource(async_session)
    await ds.make_user()
    graph_name = "DenseGraph"

    nodes = 100
    edges = 100

    graph_pyd = RedisGraph(name=graph_name)
    response = await ds.client.post(
        "/redis-graph/graph",
        headers=ds.headers["Test_user"],
        data=graph_pyd.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    graph_labels = ["location", "person", "act", "consequence"]

    for _ in range(nodes):
        node = RedisNode(
            graph=graph_name,
            label=random.choice(graph_labels),
            properties={
                "city": random_string(),
                "area": random.randint(1, 100000),
            },
        )

        response = await ds.client.post(
            "/redis-graph/node",
            headers=ds.headers["Test_user"],
            data=node.json(),
        )
        assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        f"/redis-graph/graph/{graph_name}", headers=ds.headers["Test_user"]
    )

    graph = json.loads(response.content)["item"]
    assert len(graph["nodes"]) == nodes + 1

    relation_types = ["relation", "control", "visit", "enemy"]

    for _ in range(edges):
        src = random.choice(graph["nodes"])
        dst = random.choice(graph["nodes"])

        edge = RedisEdge(
            graph=graph_name,
            source=src,
            destination=dst,
            relation=random.choice(relation_types),
        )

        response = await ds.client.post(
            "/redis-graph/edge",
            headers=ds.headers["Test_user"],
            data=edge.json(),
        )
        assert response.status_code == status.HTTP_200_OK

    response = await ds.client.get(
        f"/redis-graph/graph/{graph_name}", headers=ds.headers["Test_user"]
    )

    graph = json.loads(response.content)["item"]
    assert graph["edges"] == edges

    response = await ds.client.post(
        "/redis-graph/graph/flush",
        headers=ds.headers["Test_user"],
        data=graph_pyd.json(),
    )
    assert response.status_code == status.HTTP_200_OK

    redis_query = RedisGraphQuery(
        graph=graph_name, query="MATCH (n:location) RETURN n"
    )

    response = await ds.client.post(
        "redis-graph/graph/query",
        headers=ds.headers["Test_user"],
        data=redis_query.json(),
    )

    assert response.status_code == status.HTTP_200_OK
    assert all(
        t[0]["labels"][0] == "location"
        for t in response.json()["item"]["result"]
    )

    response = await ds.client.delete(
        f"/redis-graph/graph/{graph_name}",
        headers=ds.headers["Test_user"],
    )
    assert response.status_code == status.HTTP_200_OK
