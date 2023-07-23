"""Cassandra models module."""

from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from cassandra.cqlengine.connection import setup


from config import config
from .chat import Message, MessageBoard, ChatUser


async def get_cassandra_cluster():
    """Cassandra Connector"""

    cluster = Cluster(contact_points=[config.cassandradb_host])
    cluster.connect()
    return cluster


def initiate_cassandra():
    """Function to initiate cassandra database and models."""

    setup([config.cassandradb_host], "leafroot", retry_connect=True)

    create_keyspace_simple("leafroot", replication_factor=1)

    sync_table(MessageBoard, ["leafroot"])
    sync_table(ChatUser, ["leafroot"])
    sync_table(Message, ["leafroot"])
