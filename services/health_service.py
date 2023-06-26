from logger import log
from config import config

from sqlalchemy import create_engine
from surrealdb import Surreal
from surrealdb.ws import SurrealAuthenticationException

import redis.asyncio as redis
import pika
import motor.motor_asyncio

from utils import check_host


async def health_check():
    """Function that returns a health status.

    @returns (dict): health status

    """

    status = {}
    status["postgressql"] = await check_postgressql()
    status["redis"] = await check_redis()
    status["rabbitmq"] = await check_rabbitmq()
    status["mongo"] = await check_mongodb()
    status["spark"] = await check_host(config.spark_host)
    status["kafka"] = await check_host(config.kafka_host)
    status["surrealdb"] = await check_surrealdb()
    # status["scylladb"] = await check_scylladb()
    # status["cassandradb"] = await check_cassandradb()

    return status

@log()
async def check_surrealdb():
    """Check surrealdb database."""
    try:
        async with Surreal(config.surrealdb_url) as db:
            await db.signin({"user": config.surrealdb_user, "pass": config.surrealdb_pass,})
            await db.use(config.surrealdb_namespace, config.surrealdb_db)
            return True
    except SurrealAuthenticationException as e:
        return False
    

@log()
async def check_mongodb():
    """Checks mongo service."""

    # set a 1-second connection timeout
    client_auth = motor.motor_asyncio.AsyncIOMotorClient(
        config.mongo_url_auth, serverSelectionTimeoutMS=1000
    )
    client_no_auth = motor.motor_asyncio.AsyncIOMotorClient(
        config.mongo_url_not_auth, serverSelectionTimeoutMS=1000
    )

    error = None

    try:
        await client_auth.server_info()
        return True
    except Exception as e:
        error = e

    try:
        await client_no_auth.server_info()
        return True
    except Exception as e:
        error = e

    return str(error)


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

    redis_connection = await redis.from_url(config.redis_url)
    try:
        await redis_connection.ping()
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
