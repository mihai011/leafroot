"""Cassandra models module."""

from cassandra.cluster import Cluster

from config import config
from .chat import Message, MessageBoard, ChatUser


async def get_cassandra_connection():
    """Cassandra Connector"""

    cluster = Cluster(contact_points=[config.cassandradb_host])
    cluster.connect()
    return cluster
