"""Start of the controller module."""

import json
from typing import Annotated

from aiohttp import ClientSession
from cassandra.cluster import Cluster
from fastapi import Depends, Header
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from cache import get_redis_async_client
from data import (
    BaseResponse,
    MyIcebergCatalog,
    MyMinio,
    User,
    get_async_session,
    get_cassandra_cluster,
    get_iceberg_catalog,
    get_mongo_database,
    get_object_storage_client,
    get_sync_session,
)
from logger import log
from utils import authenthicate_user
from utils.external_api import get_http_session

CurrentAsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
CurrentSyncSession = Annotated[Session, Depends(get_sync_session)]
MongoDatabase = Annotated[AsyncIOMotorClient, Depends(get_mongo_database)]
HttpSession = Annotated[ClientSession, Depends(get_http_session)]
CassandraCluster = Annotated[Cluster, Depends(get_cassandra_cluster)]
RedisAsyncClient = Annotated[Redis, Depends(get_redis_async_client)]
ObjectStorageClient = Annotated[MyMinio, Depends(get_object_storage_client)]
IcebergCatalog = Annotated[MyIcebergCatalog, Depends(get_iceberg_catalog)]


async def auth(
    session: CurrentAsyncSession,
    authorization: str = Header(),
) -> User:
    """Auth function based on header."""
    token = authorization.split(" ")[-1]
    return await authenthicate_user(token, session)


CurrentUser = Annotated[User, Depends(auth)]


@log()
def create_response(
    message: str,
    status: int,
    response_model: BaseResponse,
    item: dict,
) -> ORJSONResponse:
    """Create a response based on response_model."""
    data = {}
    data["message"] = message
    data["item"] = item

    response = response_model(**data)

    return ORJSONResponse(status_code=status, content=json.loads(response.json()))
