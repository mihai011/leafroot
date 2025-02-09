"""Cassandraa db controllers."""

import uuid
from datetime import datetime

from data import MessageBoardResponseItem
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse
from data import (
    MessageBoard,
    Message,
    MessageBoardPacket,
    MessagePacket,
    MessageResponseItem,
)
from controllers import create_response, CurrentUser, CassandraCluster


cassandra_router = APIRouter(prefix="/cassandra", tags=["cassandra"])


@cassandra_router.post(
    "/message-board", response_model=MessageBoardResponseItem
)
async def create_message_board(
    mb: MessageBoardPacket,
    _: CurrentUser,
) -> ORJSONResponse:
    """Create message Board"""

    board_id = uuid.uuid4()
    MessageBoard.create(board_id=board_id, name=mb.name)

    return create_response(
        message="Message Board created!",
        status=status.HTTP_200_OK,
        response_model=MessageBoardResponseItem,
        item={"name": "Test", "board": board_id, "messages": []},
    )


@cassandra_router.post("/message", response_model=MessageResponseItem)
async def create_message(
    message: MessagePacket,
    user: CurrentUser,
) -> ORJSONResponse:
    """Create messsage on a board."""

    user_id = uuid.uuid4()
    message = {
        "message_id": uuid.uuid4(),
        "board_id": message.board_id,
        "user_id": user_id,
        "created_dt": uuid.uuid1(),
        "text": message.text,
    }

    msg = Message.create(**message)

    return create_response(
        message="Message Added",
        status=status.HTTP_200_OK,
        response_model=MessageResponseItem,
        item={
            "user_id": user_id,
            "message_id": msg.message_id,
            "text": msg.text,
        },
    )
