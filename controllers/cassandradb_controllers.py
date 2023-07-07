"""Cassandraa db controllers."""
from data import MessageBoardResponseItem
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from data import MessageBoard, Message, User

from controllers import create_response, CurrentUser, CassandraConnection

cassandra_router = APIRouter(prefix="/cassandra", tags=["cassandraf"])


@cassandra_router.post("/cassandra", response_model=MessageBoardResponseItem)
async def create_message_board(
    user: CurrentUser, cluster: CassandraConnection
) -> ORJSONResponse:
    """Create message Board"""

    return create_response(
        message="Message Board created!",
        status=status.HTTP_200_OK,
        response_model=MessageBoardResponseItem,
        item=None,
    )
