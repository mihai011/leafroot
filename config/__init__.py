"""Module that contains application settings."""

from typing import Literal

from pydantic import (
    Field,
    BaseSettings,
    RedisDsn,
    PostgresDsn,
    AmqpDsn,
    MongoDsn,
    AnyUrl,
)
from pydantic.typing import Optional


class Settings(BaseSettings):
    """Class responsible for loading up and generating settings."""

    app_name: str = "Fast Full API"
    env: Literal["dev", "prod"]
    domain_name: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    redis_host: str
    redis_protocol: Literal["redis", "rediss"]

    rabbitmq_host: str
    rabbitmq_protocol: Literal["amqp", "amqps"]

    sentry_dsn: AnyUrl

    access_token_expire_seconds: int
    secret_key: str
    algorithm: str
    secret: str

    interface: Optional[str]
    port: Optional[int] = Field(..., ge=1024, le=65536)

    kafka_host: Optional[str]
    kafka_url: Optional[AnyUrl]

    spark_host: Optional[str]
    spark_url: Optional[AnyUrl]

    cassandradb_host: Optional[str]

    scylladb_host: Optional[str]
    scylladb_url: Optional[AnyUrl]

    surrealdb_host: Optional[str]
    surrealdb_user: Optional[str]
    surrealdb_pass: Optional[str]
    surrealdb_namespace: Optional[str]
    surrealdb_db: Optional[str]
    surrealdb_url: Optional[AnyUrl]

    celery_broker_url: Optional[AmqpDsn]
    redis_url: Optional[RedisDsn]

    mongo_url_auth: Optional[MongoDsn]
    mongo_url_not_auth: Optional[MongoDsn]

    sqlalchemy_database_url_async: Optional[PostgresDsn]
    sqlalchemy_database_url_base_async: Optional[PostgresDsn]
    sqlalchemy_database_url_sync: Optional[PostgresDsn]
    sqlalchemy_database_url_base_sync: Optional[PostgresDsn]

    user_name: Optional[str]
    user_email: Optional[str]
    user_password: Optional[str]

    mongo_host: Optional[str]
    mongo_port: Optional[str]
    mongo_initdb_root_username: Optional[str]
    mongo_initdb_root_password: Optional[str]
    mongo_db: Optional[str]

    LOG_DIR: Optional[str] = "logs"

    INFO_LOG_FILE: Optional[str] = "info.log"
    WARN_LOG_FILE: Optional[str] = "warn.log"
    WARNING_LOG_FILE: Optional[str] = "warning.log"
    ERROR_LOG_FILE: Optional[str] = "error.log"
    DEBUG_LOG_FILE: Optional[str] = "debug.log"
    CRITICAL_LOG_FILE: Optional[str] = "critical.log"

    class Config:
        """Config class."""

        validate_assignment = True

    def __init__(self):
        super().__init__()
        self.create_celery_broker_url()
        self.create_celery_result_backend()
        self.create_database_urls()
        self.create_mongo_url()
        self.create_spark_url()
        self.create_kafka_url()
        self.create_surrealdb_url()

    def create_surrealdb_url(self):
        """Create Surrealdb url from surreal host."""
        host = self.interface or self.surrealdb_host
        self.surrealdb_url = f"http://{host}:8000"

    def create_kafka_url(self):
        """Create kafka connection url from kafka host"""
        host = self.interface or self.kafka_host
        self.kafka_url = f"aiokafka://{host}"

    def create_spark_url(self):
        """Create spark conection url"""
        host = self.interface or self.spark_host

        self.spark_url = f"spark://{host}"

    def create_mongo_url(self):
        """Create the connection url for mongo."""
        host = self.interface or self.mongo_host

        self.mongo_url_auth = "mongodb://{}:{}@{}:{}".format(
            self.mongo_initdb_root_username,
            self.mongo_initdb_root_password,
            host,
            self.mongo_port,
        )

        self.mongo_url_not_auth = "mongodb://{}:{}".format(
            host, self.mongo_port
        )

    def create_celery_broker_url(self):
        """Create the url for the celery broker."""
        host = self.interface or self.rabbitmq_host
        self.celery_broker_url = "{}://{}:5672".format(
            self.rabbitmq_protocol, host
        )

    def create_celery_result_backend(self):
        """Create the url for the celery backend."""
        host = self.interface or self.redis_host
        self.redis_url = "{}://{}:6379".format(self.redis_protocol, host)

    def create_database_urls(self):
        """Create the database urls."""
        host = self.interface or self.postgres_host
        self.sqlalchemy_database_url_async = "{}://{}:{}@{}/{}".format(
            "postgresql+asyncpg",
            self.postgres_user,
            self.postgres_password,
            host,
            self.postgres_db,
        )

        self.sqlalchemy_database_url_base_async = "{}://{}:{}@{}/".format(
            "postgresql+asyncpg",
            self.postgres_user,
            self.postgres_password,
            host,
        )

        self.sqlalchemy_database_url_sync = "{}://{}:{}@{}/{}".format(
            "postgresql",
            self.postgres_user,
            self.postgres_password,
            host,
            self.postgres_db,
        )

        self.sqlalchemy_database_url_base_sync = "{}://{}:{}@{}/".format(
            "postgresql",
            self.postgres_user,
            self.postgres_password,
            host,
        )


config = Settings()
