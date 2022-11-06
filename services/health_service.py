from logger import log
from config import config

from sqlalchemy import create_engine
import redis
import pika


async def health_check():
    """Function that returns a health status.

    @returns (dict): health status

    """

    status = {}
    status["postgressql"] = await check_postgressql()
    status["redis"] = await check_redis()
    status["rabbitmq"] = await check_rabbitmq()
    return status


@log()
async def check_postgressql():
    """Check postgresql connection"""

    engine = create_engine(config.sqlalchemy_database_url_base_sync)
    try:
        with engine.connect() as _:
            return True
    except Exception as e:
        return str(e)


@log()
async def check_redis():
    """Check redis connection"""

    redis_connection = redis.from_url(config.redis_url)
    try:
        redis_connection.set("test", "test")
        return True
    except Exception as e:
        return str(e)


@log()
async def check_rabbitmq():
    """Check rabbitmq connection."""

    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(config.celery_broker_url)
        )
        channel = connection.channel()
        channel.basic_publish(
            exchange="test", routing_key="test", body=b"Test message."
        )
        connection.close()
        return True
    except Exception as e:
        return str(e)
