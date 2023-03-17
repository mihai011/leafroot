"""Module for related data."""

from enum import Enum
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel, HttpUrl
from pydantic.typing import Dict

from data.models.postgresql import Base
from data.models.postgresql.user import User
from data.models.postgresql.atom import Atom, Electron, Neutron, Proton
from data.models.postgresql import get_session, async_session
from data.models.redis_db import (
    get_redis_connection,
    RedisGraph,
    RedisNode,
    RedisEdge,
    RedisGraphQuery,
)
from config import config
from logger import log


@log()
def create_database_app():
    """Create database with db_name."""

    DB_URL_BASE_SYNC = "{}{}".format(
        config.sqlalchemy_database_url_base_sync, config.postgres_db
    )

    if not database_exists(DB_URL_BASE_SYNC):
        create_database(DB_URL_BASE_SYNC)
        return True

    return False


@log()
def create_mongodb_schemas():
    """Create MongoDB databases."""


class HttpMethodsModel(str, Enum):
    """Enum class for http methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class HttpRequest(BaseModel):
    """HttpRequest Model class."""

    method: HttpMethodsModel
    url: HttpUrl
    params: Dict[str, str]
    body: str
    headers: Dict[str, str]

    class Config:
        """Config class for HttpRequestModel"""

        use_enum_values = True
