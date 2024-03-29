"""Models and utils functions for redsi."""

import redis
from redis import Redis

from config import config
from logger import log
from .graph import RedisGraph, RedisNode, RedisEdge, RedisGraphQuery


@log()
def get_redis_connection() -> Redis:
    """Yields and redis connection object."""
    try:
        with redis.from_url(config.redis_url) as connection:
            yield connection
    finally:
        connection.close()
