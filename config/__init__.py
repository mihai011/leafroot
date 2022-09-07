"""module that contains application settings"""

from typing import Literal

from pydantic import BaseSettings, RedisDsn, PostgresDsn, AmqpDsn
from pydantic.typing import Optional


class Settings(BaseSettings):
    """class responsible for loading up and generating settings

    Args:
        BaseSettings (_type_): _description_
    """

    app_name: str = "Fast Full API"
    env: Literal["dev", "prod"]
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str

    redis_host: str
    redis_protocol: Literal["redis", "rediss"]

    rabbitmq_host: str
    rabbitmq_protocol: Literal["amqp", "amqps"]

    access_token_expire_minutes: str
    secret_key: str
    algorithm: str
    secret: str

    interface: Optional[str]

    celery_broker_url: Optional[AmqpDsn]
    redis_url: Optional[RedisDsn]

    sqlalchemy_database_url_async: Optional[PostgresDsn]
    sqlalchemy_database_url_base_async: Optional[PostgresDsn]
    sqlalchemy_database_url_sync: Optional[PostgresDsn]
    sqlalchemy_database_url_base_sync: Optional[PostgresDsn]

    class Config:
        """class config"""

        env_file = ".env_user"
        env_file_encoding = "utf-8"
        validate_assignment = True

    def __init__(self):

        super().__init__()
        self.create_celery_broker_url()
        self.create_celery_result_backend()
        self.create_database_urls()

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
