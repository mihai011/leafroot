"""Module for related data."""

from sqlalchemy_utils import database_exists, create_database

from data.models.postgresql import Base
from data.models.postgresql.user import User
from data.models.postgresql.atom import Atom, Electron, Neutron, Proton
from data.models.postgresql import get_session, async_session
from data.models.redis_db import get_redis_connection, RedisGraph, RedisNode
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
