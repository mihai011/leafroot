"""Start of the controller module."""


from typing import Annotated

from aiohttp import ClientSession
from fastapi.responses import ORJSONResponse
from fastapi import Header, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient
from cassandra.cluster import Cluster
from redis.asyncio import Redis
from cache import get_redis_async_client

from data import (
    User,
    BaseResponse,
    MyMinio,
    get_async_session,
    get_sync_session,
    get_mongo_database,
    get_cassandra_cluster,
    get_object_storage_client,
)
from utils.external_api import get_http_session
from utils import authenthicate_user
from logger import log

CurrentAsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
CurrentSyncSession = Annotated[Session, Depends(get_sync_session)]
MongoDatabase = Annotated[AsyncIOMotorClient, Depends(get_mongo_database)]
HttpSession = Annotated[ClientSession, Depends(get_http_session)]
CassandraCluster = Annotated[Cluster, Depends(get_cassandra_cluster)]
RedisAsyncClient = Annotated[Redis, Depends(get_redis_async_client)]
ObjectStorageClient = Annotated[MyMinio, Depends(get_object_storage_client)]


async def auth(
    session: CurrentAsyncSession,
    authorization: str = Header(),
):
    """Auth function based on header."""
    token = authorization.split(" ")[-1]
    return await authenthicate_user(token, session)


CurrentUser = Annotated[User, Depends(auth)]


@log()
def create_response(
    message: str, status: int, response_model: BaseResponse, item=None
) -> ORJSONResponse:
    """Receive a message parameter from which a reponse is created and item
    from wich a dictionay is ORJSONResponse object is made as response."""
    data = {}
    data["message"] = message
    data["item"] = item

    response = response_model(**data)

    return ORJSONResponse(status_code=status, content=response.dict())
