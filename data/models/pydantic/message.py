"""Mesage Board Packet model."""

from pydantic import UUID4, BaseModel


class MessageBoardPacket(BaseModel):
    """Message Board Packet."""

    name: str


class MessagePacket(BaseModel):
    """Message Packet."""

    text: str
    board_id: UUID4


class ChatUser(BaseModel):
    """CharUser Packet."""

    username: str
