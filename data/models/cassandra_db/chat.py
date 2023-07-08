from enum import unique

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from sqlalchemy import column

from config import config


class MessageBoard(Model):
    board_id = columns.UUID(primary_key=True)
    name = columns.Text()


class ChatUser(Model):
    user_id = columns.UUID(primary_key=True)
    username = columns.Text()


class Message(Model):
    message_id = columns.UUID(primary_key=True)
    board_id = columns.UUID()
    user_id = columns.UUID()
    created_dt = columns.TimeUUID()
    text = columns.Text()
