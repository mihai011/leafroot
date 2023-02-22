"""
Models and utils functions for redsi
"""
from config import config
from .graph import RedisGraph, RedisNode, RedisEdge
from logger import log

import redis
from redis import Redis


def get_redis_connection() -> Redis:
    """
    Yields and redis connection object.
    """
    try:
        with redis.from_url(config.redis_url) as connection:
            yield connection
    finally:
        connection.close()
