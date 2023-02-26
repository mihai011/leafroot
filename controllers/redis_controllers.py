"""Redis controllers."""
import logging

from fastapi import Request, APIRouter, Depends, Body
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from data import (
    get_session,
    get_redis_connection,
    RedisGraph,
    RedisNode,
    RedisEdge,
)
from external_api.utils import get_http_session, make_api_request
from controllers import create_response, auth_decorator, parse

from services.redis_service import redis_service

redis_router = APIRouter(prefix="/redis-graph", tags=["redis"])


@redis_router.get("/graph/{graph_name}")
@auth_decorator
async def get_redis_graph(
    graph_name: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    graph = redis_service.get_graph_metadata(graph_name)
    return create_response("Graph created!", 200, graph)


@redis_router.delete("/graph/{graph_name}")
@auth_decorator
async def delete_redis_graph(
    graph_name: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """Delete a graph."""

    redis_service.delete_graph(graph_name)
    return create_response("Graph deleted!", 200)


@redis_router.post("/graph/commit")
@auth_decorator
async def commit_redis_graph(
    request: Request,
    session: AsyncSession = Depends(get_session),
    graph: RedisGraph = Body(...),
) -> ORJSONResponse:
    """Commit contents of a graph to Redis."""

    graph = redis_service.graph_commit(graph)
    return create_response("Graph commited!", 200)


@redis_router.post("/graph")
@auth_decorator
async def redis_graph(
    request: Request,
    session: AsyncSession = Depends(get_session),
    graph: RedisGraph = Body(...),
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    graph = redis_service.add_graph(graph)
    return create_response("Graph created!", 200, graph)


@redis_router.post("/node")
@auth_decorator
async def redis_node(
    request: Request,
    session: AsyncSession = Depends(get_session),
    node: RedisNode = Body(...),
) -> ORJSONResponse:
    """Add a node to a graph."""

    node = redis_service.add_node_to_graph(node)
    return create_response("Node created and added!", 200, node)


@redis_router.post("/edge")
@auth_decorator
async def redis_node(
    request: Request,
    session: AsyncSession = Depends(get_session),
    redis_client=Depends(get_redis_connection),
    edge: RedisEdge = Body(...),
) -> ORJSONResponse:
    """Add an edge to a graph."""

    edge = redis_service.add_edge_to_graph(edge)
    return create_response("Node created and added!", 200, edge)
