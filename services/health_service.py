"""Module for checking the health of required services."""

from __future__ import annotations

import motor.motor_asyncio
import pika
import redis.asyncio as redis
import timeout_decorator
from cassandra import UnresolvableContactPoints
from cassandra.cluster import Cluster
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from pika.exceptions import AMQPConnectionError
from pyspark.errors.exceptions.connect import SparkConnectGrpcException
from pyspark.sql import SparkSession
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from surrealdb import Surreal

from config import config
from logger import log


async def health_check() -> dict:
    """Function that returns a health status.

    @returns (dict): health status

    """
    status = {}
    status["postgressql"] = await check_postgressql()
    status["redis"] = await check_redis()
    status["rabbitmq"] = await check_rabbitmq()
    status["mongo"] = await check_mongodb()
    status["spark"] = True  # check_spark()
    status["kafka"] = True  # check_kafka()
    status["surrealdb"] = True  # await check_surrealdb()
    status["scylladb"] = True  # await check_scylladb()
    status["cassandradb"] = True  # await check_cassandradb()

    return status


@log()
def check_kafka() -> bool:
    """Check connection to kafka cluster."""
    try:
        producer = KafkaProducer(bootstrap_servers=config.kafka_host)
        producer.metrics()
    except NoBrokersAvailable:
        return False
    return True


@log()
def check_spark() -> bool:
    """Check connection to spark cluster."""

    @timeout_decorator.timeout(5)
    def try_connect() -> None:
        """Try to connect to spark."""
        spark = SparkSession.builder.remote(f"sc://{config.spark_host}").getOrCreate()

        sample_data = [
            {"name": "John    D.", "age": 30},
            {"name": "Alice   G.", "age": 25},
            {"name": "Bob  T.", "age": 35},
            {"name": "Eve   A.", "age": 28},
        ]

        df = spark.createDataFrame(sample_data)
        df.show()

    try:
        try_connect()
    except SparkConnectGrpcException:
        return False

    return True


@log()
async def check_cassandradb() -> bool | None:
    """Check cassandradb cluster."""
    try:
        cluster = Cluster(contact_points=[config.cassandradb_host])
        cluster.connect()
    except UnresolvableContactPoints:
        return False
    return True


@log()
async def check_scylladb() -> bool | None:
    """Check scylladb cluster."""
    try:
        cluster = Cluster(contact_points=[config.scylladb_host])
        cluster.connect()
    except UnresolvableContactPoints:
        return False
    return True


@log()
async def check_surrealdb() -> bool | None:
    """Check surrealdb database."""
    try:
        async with Surreal(config.surrealdb_url) as db:
            await db.signin(
                {
                    "user": config.surrealdb_user,
                    "pass": config.surrealdb_pass,
                },
            )
            await db.use(config.surrealdb_namespace, config.surrealdb_db)

    except ConnectionRefusedError:
        return False
    return True


@log()
async def check_mongodb() -> bool:
    """Checks mongo service."""
    # set a 1-second connection timeout
    client_auth = motor.motor_asyncio.AsyncIOMotorClient(
        config.mongo_url_auth,
        serverSelectionTimeoutMS=1000,
    )

    await client_auth.server_info()
    return True


@log()
async def check_postgressql() -> bool | None:
    """Check postgresql connection."""
    engine = create_engine(config.sqlalchemy_database_url_base_sync)
    try:
        engine.connect()
    except SQLAlchemyError:
        return False
    return True


@log()
async def check_redis() -> bool | None:
    """Check redis connection."""
    redis_connection = await redis.from_url(config.redis_url)
    try:
        await redis_connection.ping()
    except ConnectionError:
        return False
    return True


@log()
async def check_rabbitmq() -> bool | None:
    """Check rabbitmq connection."""
    try:
        connection = pika.BlockingConnection(
            pika.URLParameters(config.celery_broker_url),
        )
        channel = connection.channel()
        channel.basic_publish(
            exchange="test",
            routing_key="test",
            body=b"Test message.",
        )
        connection.close()
    except AMQPConnectionError:
        return False

    return True
