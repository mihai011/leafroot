"""Cassandra Models."""

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class MessageBoard(Model):
    """Model for message board."""

    board_id = columns.UUID(primary_key=True)
    name = columns.Text()


class ChatUser(Model):
    """Model for char user."""

    user_id = columns.UUID(primary_key=True)
    username = columns.Text()


class Message(Model):
    """Model for chat messager."""

    message_id = columns.UUID(primary_key=True)
    board_id = columns.UUID()
    user_id = columns.UUID()
    created_dt = columns.TimeUUID()
    text = columns.Text()
