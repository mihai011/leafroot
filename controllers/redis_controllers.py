"""Redis controllers."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from data import (
    RedisGraph,
    RedisNode,
    RedisEdge,
    RedisGraphQuery,
    RedisGraphResponseItem,
    BaseResponse,
    RedisNodeResponseItem,
    RedisQueryResponseItem,
)
from controllers import create_response, CurrentUser

from services.redis_service import redis_service

redis_router = APIRouter(prefix="/redis-graph", tags=["redis"])


@redis_router.get("/graph/{graph_name}", response_model=RedisGraphResponseItem)
async def get_redis_graph(
    graph_name: str,
    _: CurrentUser,
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    graph = redis_service.get_graph_metadata(graph_name)
    return create_response(
        message="Graph created!",
        status=status.HTTP_200_OK,
        response_model=RedisGraphResponseItem,
        item=graph,
    )


@redis_router.delete("/graph/{graph_name}", response_model=BaseResponse)
async def delete_redis_graph(
    graph_name: str,
    _: CurrentUser,
) -> ORJSONResponse:
    """Delete a graph."""

    redis_service.delete_graph(graph_name)
    return create_response(
        message="Graph deleted!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item="True",
    )


@redis_router.post("/graph/flush", response_model=BaseResponse)
async def flush_redis_graph(
    _: CurrentUser, graph: RedisGraph
) -> ORJSONResponse:
    """Flush contents of a graph to Redis."""

    redis_service.graph_flush(graph)
    return create_response(
        message="Graph flushed!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item="True",
    )


@redis_router.post("/graph", response_model=RedisGraphResponseItem)
async def redis_graph(
    _: CurrentUser,
    graph: RedisGraph,
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    graph = redis_service.add_graph(graph)
    return create_response(
        message="Graph created!",
        status=status.HTTP_200_OK,
        response_model=RedisGraphResponseItem,
        item=graph,
    )


@redis_router.post("/node", response_model=RedisNodeResponseItem)
async def redis_node(
    _: CurrentUser,
    node: RedisNode,
) -> ORJSONResponse:
    """Add a node to a graph."""

    node = redis_service.add_node_to_graph(node)
    return create_response(
        message="Node created and added!",
        status=status.HTTP_200_OK,
        response_model=RedisNodeResponseItem,
        item=node,
    )


@redis_router.post("/edge", response_model=BaseResponse)
async def redis_edge(
    _: CurrentUser,
    edge: RedisEdge,
) -> ORJSONResponse:
    """Add an edge to a graph."""

    redis_service.add_edge_to_graph(edge)
    return create_response(
        message="Edge created and added!",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item="True",
    )


@redis_router.post("/graph/query", response_model=RedisQueryResponseItem)
async def redis_graph_query(
    _: CurrentUser,
    query: RedisGraphQuery,
) -> ORJSONResponse:
    """Makes a query to redis graph."""

    result = redis_service.graph_query(query)
    result = {"result": result}
    return create_response(
        message="Redis Query made!",
        status=status.HTTP_200_OK,
        response_model=RedisQueryResponseItem,
        item=result,
    )
