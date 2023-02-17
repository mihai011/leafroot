"""
Models and utils functions for redsi
"""
import config

import redis.asyncio as redis
from redis.asyncio.client import Redis


async def get_redis_connection() -> Redis:
    """
    Yields and redis connection object.
    """
    try:
        async with redis.from_url(config.redis_url) as connection:
            yield connection
    finally:
        await connection.close()
