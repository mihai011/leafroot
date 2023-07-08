"""Module for related data."""

from enum import Enum
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel, HttpUrl
from pydantic.typing import Dict

from data.models.postgresql import Base
from data.models.postgresql.user import User
from data.models.postgresql.atom import Atom, Electron, Neutron, Proton
from data.models.postgresql.glovo import (
    Product,
    Curier,
    Restaurant,
    Order,
    OrderItem,
)
from data.models.postgresql import (
    get_async_session,
    async_session,
    get_sync_session,
)
from data.models.redis_db import (
    get_redis_connection,
    RedisGraph,
    RedisNode,
    RedisEdge,
    RedisGraphQuery,
)
from data.models.pydantic import (
    MessagePacket,
    MessageBoardPacket,
    MessageBoardResponseItem,
    MessageResponseItem,
    PydanticAtom,
    PydanticElectron,
    PydanticNeutron,
    PydanticProton,
    UserResponse,
    BaseResponse,
    ErrorResponse,
    UserResponseItem,
    AuthorizedUserResponseItem,
    StatusResponseItem,
    PydanticQuote,
    QuoteResponseItem,
    TaskResponseItem,
    BookListResponseItem,
    ParticleResponseItem,
    AtomResponseItem,
    ParticleResponseListItem,
    RedisGraphResponseItem,
    RedisNodeResponseItem,
    RedisQueryResponseItem,
)
from data.models.mongo_db.library import Library, Book, BookUpdate, BookPackage
from data.models.mongo_db import get_mongo_database, get_mongo_client

from data.models.cassandra_db import (
    MessageBoard,
    ChatUser,
    Message,
    get_cassandra_cluster,
    initiate_cassandra,
)

from data.models.users import PydanticUser, PydanticUserSignUp
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
        """Config class for HttpRequestModel."""

        use_enum_values = True
