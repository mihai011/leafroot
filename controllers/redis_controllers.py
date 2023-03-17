"""Redis controllers."""

from fastapi import APIRouter, Depends, Body
from fastapi.responses import ORJSONResponse

from data import (
    RedisGraph,
    RedisNode,
    RedisEdge,
    RedisGraphQuery,
)
from controllers import create_response, auth

from services.redis_service import redis_service

redis_router = APIRouter(prefix="/redis-graph", tags=["redis"])


@redis_router.get("/graph/{graph_name}")
async def get_redis_graph(
    graph_name: str,
    payload: dict = Depends(auth),
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    graph = redis_service.get_graph_metadata(graph_name)
    return create_response("Graph created!", 200, graph)


@redis_router.delete("/graph/{graph_name}")
async def delete_redis_graph(
    graph_name: str,
    payload: dict = Depends(auth),
) -> ORJSONResponse:
    """Delete a graph."""

    redis_service.delete_graph(graph_name)
    return create_response("Graph deleted!", 200)


@redis_router.post("/graph/flush")
async def flush_redis_graph(
    payload: dict = Depends(auth),
    graph: RedisGraph = Body(...),
) -> ORJSONResponse:
    """Flush contents of a graph to Redis."""

    graph = redis_service.graph_flush(graph)
    return create_response("Graph flushed!", 200)


@redis_router.post("/graph")
async def redis_graph(
    payload: dict = Depends(auth),
    graph: RedisGraph = Body(...),
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    graph = redis_service.add_graph(graph)
    return create_response("Graph created!", 200, graph)


@redis_router.post("/node")
async def redis_node(
    payload: dict = Depends(auth),
    node: RedisNode = Body(...),
) -> ORJSONResponse:
    """Add a node to a graph."""

    node = redis_service.add_node_to_graph(node)
    return create_response("Node created and added!", 200, node)


@redis_router.post("/edge")
async def redis_edge(
    payload: dict = Depends(auth),
    edge: RedisEdge = Body(...),
) -> ORJSONResponse:
    """Add an edge to a graph."""

    edge = redis_service.add_edge_to_graph(edge)
    return create_response("Edge created and added!", 200, edge)


@redis_router.post("/graph/query")
async def redis_graph_query(
    payload: dict = Depends(auth),
    query: RedisGraphQuery = Body(...),
) -> ORJSONResponse:
    """Makes a query to redis graph."""

    result = redis_service.graph_query(query)
    return create_response("Redis Query made!", 200, result)