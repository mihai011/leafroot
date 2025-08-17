"""Module for related data."""

from enum import Enum

from pydantic import BaseModel, HttpUrl
from sqlalchemy_utils import create_database, database_exists

from config import config
from data.models.cassandra_db import (
    ChatUser,
    Message,
    MessageBoard,
    get_cassandra_cluster,
    initiate_cassandra,
)
from data.models.iceberg import MyIcebergCatalog, get_iceberg_catalog
from data.models.minio import MyMinio, get_minio_client, get_object_storage_client
from data.models.mongo_db import get_mongo_client, get_mongo_database
from data.models.mongo_db.library import Book, BookPackage, BookUpdate, Library
from data.models.postgresql import (
    Base,
    ExtraBase,
    async_session,
    get_async_session,
    get_sync_session,
)
from data.models.postgresql.atom import Atom, Electron, Neutron, Proton
from data.models.postgresql.glovo import (
    Curier,
    Order,
    OrderItem,
    Product,
    Restaurant,
)
from data.models.postgresql.photos import Photo
from data.models.postgresql.quote import Quote
from data.models.postgresql.user import User, UserFollowRelation
from data.models.pydantic import (
    AtomResponseItem,
    AuthorizedUserResponseItem,
    BaseResponse,
    BookListResponseItem,
    ErrorResponse,
    KeyValuePacket,
    MessageBoardPacket,
    MessageBoardResponseItem,
    MessagePacket,
    MessageResponseItem,
    ParticleResponseItem,
    ParticleResponseListItem,
    PhotoInfoResponse,
    PhotoInfoResponseItem,
    PhotoPacket,
    PhotoResponse,
    PhotoResponseItem,
    PhotoResponseListItem,
    PydanticAtom,
    PydanticElectron,
    PydanticNeutron,
    PydanticProton,
    PydanticQuote,
    QuoteResponseItem,
    RedisGraphResponseItem,
    RedisNodeResponseItem,
    RedisQueryResponseItem,
    StatusResponseItem,
    TaskResponseItem,
    UrlPacket,
    UrlShortResponseItem,
    UserResponse,
    UserResponseItem,
)
from data.models.redis_db import (
    RedisEdge,
    RedisGraph,
    RedisGraphQuery,
    RedisNode,
    get_redis_connection,
)
from data.models.users import PydanticUser, PydanticUserSignUp
from logger import log

__all__ = [
    "Atom",
    "Electron",
    "Neutron",
    "Proton",
    "MyIcebergCatalog",
    "get_iceberg_catalog",
    "get_object_storage_client",
    "get_mongo_client",
    "get_minio_client",
    "get_mongo_database",
    "MyMinio",
    "Book",
    "BookPackage",
    "BookUpdate",
    "Photo",
    "Quote",
    "Library",
    "Curier",
    "Order",
    "OrderItem",
    "Product",
    "Restaurant",
    "AtomResponseItem",
    "AuthorizedUserResponseItem",
    "BaseResponse",
    "BookListResponseItem",
    "ErrorResponse",
    "KeyValuePacket",
    "MessageBoardPacket",
    "MessageBoardResponseItem",
    "MessagePacket",
    "MessageResponseItem",
    "ParticleResponseItem",
    "ParticleResponseListItem",
    "PhotoInfoResponse",
    "PhotoInfoResponseItem",
    "PhotoPacket",
    "PhotoResponse",
    "PhotoResponseItem",
    "PhotoResponseListItem",
    "PydanticAtom",
    "PydanticElectron",
    "PydanticNeutron",
    "PydanticProton",
    "PydanticQuote",
    "QuoteResponseItem",
    "RedisGraphResponseItem",
    "RedisNodeResponseItem",
    "RedisQueryResponseItem",
    "StatusResponseItem",
    "TaskResponseItem",
    "UrlPacket",
    "UrlShortResponseItem",
    "UserResponse",
    "UserResponseItem",
    "PydanticUser",
    "PydanticUserSignUp",
    "RedisEdge",
    "RedisGraph",
    "RedisGraphQuery",
    "RedisNode",
    "get_redis_connection",
    "User",
    "UserFollowRelation",
    "ChatUser",
    "Message",
    "MessageBoard",
    "get_cassandra_cluster",
    "initiate_cassandra",
    "Base",
    "ExtraBase",
    "async_session",
    "get_async_session",
    "get_sync_session",
]


@log()
def create_database_app() -> bool:
    """Create database with db_name."""
    db_url_base_sync = f"{config.sqlalchemy_database_url_base_sync}{config.postgres_db}"

    if not database_exists(db_url_base_sync):
        create_database(db_url_base_sync)
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
    params: dict[str, str]
    body: str
    headers: dict[str, str]

    class Config:
        """Config class for HttpRequestModel."""

        use_enum_values = True
