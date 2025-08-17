"""Module that contains application settings."""

from __future__ import annotations

from typing import Literal

from pydantic import (
    AmqpDsn,
    AnyUrl,
    Field,
    HttpUrl,
    MongoDsn,
    PostgresDsn,
    RedisDsn,
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
    rabbitmq_default_user: str
    rabbitmq_default_pass: str

    sentry_dsn: AnyUrl

    access_token_expire_seconds: int
    secret_key: str
    algorithm: str
    secret: str

    interface: str | None
    port: int | None = Field(..., ge=1024, le=65536)

    kafka_host: str | None

    spark_host: str | None

    cassandradb_host: str | None

    scylladb_host: str | None

    surrealdb_host: str | None
    surrealdb_port: str | None
    surrealdb_user: str | None
    surrealdb_pass: str | None
    surrealdb_namespace: str | None
    surrealdb_db: str | None

    user_name: str | None
    user_email: str | None
    user_password: str | None

    mongo_host: str | None
    mongo_port: str | None
    mongo_initdb_root_username: str | None
    mongo_initdb_root_password: str | None
    mongo_db: str | None

    minio_root_user: str
    minio_root_password: str
    minio_host: str
    minio_port: str
    minio_bucket: str
    minio_secure: bool
    minio_access_key: str
    minio_secret_key: str

    LOG_DIR: str | None = "logs"

    INFO_LOG_FILE: str | None = "info.log"
    WARN_LOG_FILE: str | None = "warn.log"
    WARNING_LOG_FILE: str | None = "warning.log"
    ERROR_LOG_FILE: str | None = "error.log"
    DEBUG_LOG_FILE: str | None = "debug.log"
    CRITICAL_LOG_FILE: str | None = "critical.log"

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
        """Create kafka connection url from kafka host."""
        host = self.interface or self.kafka_host
        return f"aiokafka://{host}"

    @computed_field
    def spark_url(self) -> AnyUrl:
        """Create spark conection url."""
        host = self.interface or self.spark_host
        return f"spark://{host}"

    @computed_field
    def mongo_url_auth(self) -> AnyUrl:
        """Create the connection url for mongo."""
        host = self.interface or self.mongo_host

        return f"mongodb://{self.mongo_initdb_root_username}:{self.mongo_initdb_root_password}@{host}:{self.mongo_port}"

    @computed_field
    def mongo_url_not_auth(self) -> MongoDsn:
        """Create the connection not auth url for mongo."""
        host = self.interface or self.mongo_host
        return f"mongodb://{host}:{self.mongo_port}"

    @computed_field
    def celery_broker_url(self) -> AmqpDsn:
        """Create the url for the celery broker."""
        host = self.interface or self.rabbitmq_host
        return f"{self.rabbitmq_protocol}://{config.rabbitmq_default_user}:{config.rabbitmq_default_pass}@{host}:5672"

    @computed_field
    def redis_url(self) -> RedisDsn:
        """Create the url for the celery backend."""
        host = self.interface or self.redis_host
        return f"{self.redis_protocol}://{host}:6379"

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
