from enum import unique
import re
from cassandra.cqlengine import columns
from cassandra.cqlengine.connection import setup
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from sqlalchemy import column

from config import config

setup([config.cassandradb_host], "leafroot", retry_connect=True)

create_keyspace_simple("leafroot", replication_factor=1)


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


sync_table(MessageBoard)
sync_table(ChatUser)
sync_table(Message)
