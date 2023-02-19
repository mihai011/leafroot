"""Redis controllers."""
import logging

from fastapi import Request, APIRouter, Depends, Body
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.commands.graph.node import Node

from data import get_session, get_redis_connection, RedisGraph
from external_api.utils import get_http_session, make_api_request
from controllers import create_response, auth_decorator, parse

redis_router = APIRouter(prefix="/redis", tags=["redis"])


@redis_router.post("/graph")
@auth_decorator
async def redis_graph(
    request: Request,
    session: AsyncSession = Depends(get_session),
    redis_client=Depends(get_redis_connection),
    graph: RedisGraph = Body(...),
) -> ORJSONResponse:
    """Make a graph into redis with a single dummy node."""

    g = redis_client.graph(graph.name)

    if len(g.nodes) == 0:
        dummy_node = Node(label="DUMMY", properties={})
        g.add_node(dummy_node)
    g.commit()

    return create_response("Graph created!", 200)
