"""Module that contains application settings."""

from typing import Literal, Optional

from pydantic import (
    Field,
    RedisDsn,
    PostgresDsn,
    AmqpDsn,
    MongoDsn,
    AnyUrl,
    HttpUrl,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Class responsible for loading up and generating settings."""

    model_config = SettingsConfigDict(case_sensitive=False)

    app_name: str = "Fast Full API"
    env: Literal["dev", "prod", "circle"]
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
    # kafka_url: Optional[AnyUrl]

    spark_host: Optional[str]
    # spark_url: Optional[AnyUrl]

    cassandradb_host: Optional[str]

    scylladb_host: Optional[str]
    # scylladb_url: Optional[AnyUrl]

    surrealdb_host: Optional[str]
    surrealdb_port: Optional[str]
    surrealdb_user: Optional[str]
    surrealdb_pass: Optional[str]
    surrealdb_namespace: Optional[str]
    surrealdb_db: Optional[str]

    user_name: Optional[str]
    user_email: Optional[str]
    user_password: Optional[str]

    mongo_host: Optional[str]
    mongo_port: Optional[str]
    mongo_initdb_root_username: Optional[str]
    mongo_initdb_root_password: Optional[str]
    mongo_db: Optional[str]

    minio_root_user: str
    minio_root_password: str
    minio_host: str
    minio_port: str
    # minio_url: Optional[str]
    minio_bucket: str
    minio_secure: bool
    minio_access_key: str
    minio_secret_key: str

    LOG_DIR: Optional[str] = "logs"

    INFO_LOG_FILE: Optional[str] = "info.log"
    WARN_LOG_FILE: Optional[str] = "warn.log"
    WARNING_LOG_FILE: Optional[str] = "warning.log"
    ERROR_LOG_FILE: Optional[str] = "error.log"
    DEBUG_LOG_FILE: Optional[str] = "debug.log"
    CRITICAL_LOG_FILE: Optional[str] = "critical.log"

    @computed_field
    def minio_url(self) -> AnyUrl:
        """Create minio url from minio host and minio port."""
        host = self.interface or self.minio_host
        return f"{host}:{self.minio_port}"

    @computed_field
    def surrealdb_url(self) -> AnyUrl:
        """Create Surrealdb url from surreal host."""
        host = self.interface or self.surrealdb_host
        return f"http://{host}:{self.surrealdb_port}"

    @computed_field
    def kafka_url(self) -> AnyUrl:
        """Create kafka connection url from kafka host"""
        host = self.interface or self.kafka_host
        return f"aiokafka://{host}"

    @computed_field
    def spark_url(self) -> AnyUrl:
        """Create spark conection url"""
        host = self.interface or self.spark_host
        return f"spark://{host}"

    @computed_field
    def mongo_url_auth(self) -> AnyUrl:
        """Create the connection url for mongo."""
        host = self.interface or self.mongo_host

        return "mongodb://{}:{}@{}:{}".format(
            self.mongo_initdb_root_username,
            self.mongo_initdb_root_password,
            host,
            self.mongo_port,
        )

    @computed_field
    def mongo_url_not_auth(self) -> MongoDsn:
        """Create the connection not auth url for mongo."""

        host = self.interface or self.mongo_host
        return "mongodb://{}:{}".format(host, self.mongo_port)

    @computed_field
    def celery_broker_url(self) -> AmqpDsn:
        """Create the url for the celery broker."""

        host = self.interface or self.rabbitmq_host
        return "{}://{}:5672".format(self.rabbitmq_protocol, host)

    @computed_field
    def redis_url(self) -> RedisDsn:
        """Create the url for the celery backend."""

        host = self.interface or self.redis_host
        return "{}://{}:6379".format(self.redis_protocol, host)

    @computed_field
    def sqlalchemy_database_url_async(self) -> PostgresDsn:
        """Create the database urls."""

        host = self.interface or self.postgres_host
        return "{}://{}:{}@{}/{}".format(
            "postgresql+asyncpg",
            self.postgres_user,
            self.postgres_password,
            host,
            self.postgres_db,
        )

    @computed_field
    def sqlalchemy_database_url_base_async(self) -> PostgresDsn:
        """Create the base url for the async database."""

        host = self.interface or self.postgres_host
        return "{}://{}:{}@{}/".format(
            "postgresql+asyncpg",
            self.postgres_user,
            self.postgres_password,
            host,
        )

    @computed_field
    def sqlalchemy_database_url_sync(self) -> PostgresDsn:
        """Created the base url for the sync database."""

        host = self.interface or self.postgres_host
        return "{}://{}:{}@{}/{}".format(
            "postgresql",
            self.postgres_user,
            self.postgres_password,
            host,
            self.postgres_db,
        )

    @computed_field
    def sqlalchemy_database_url_base_sync(self) -> PostgresDsn:
        """Created the base url for the sync database."""
        host = self.interface or self.postgres_host
        return "{}://{}:{}@{}/".format(
            "postgresql",
            self.postgres_user,
            self.postgres_password,
            host,
        )

    @computed_field
    def s3_endpoint(self) -> HttpUrl:
        """Create the s3 endpoint."""
        return f"http://{self.minio_host}:{self.minio_port}"


config = Settings()
