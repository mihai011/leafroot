"""Start of the controller module."""


from typing import Annotated

from aiohttp import ClientSession
from fastapi.responses import ORJSONResponse
from fastapi import Header, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient

from data import (
    User,
    get_async_session,
    get_sync_session,
    get_mongo_database,
    BaseResponse,
)
from utils.external_api import get_http_session
from utils import authenthicate_user
from logger import log

CurrentAsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
CurrentSyncSession = Annotated[Session, Depends(get_sync_session)]
MongoDatabase = Annotated[AsyncIOMotorClient, Depends(get_mongo_database)]
HttpSession = Annotated[ClientSession, Depends(get_http_session)]


@log()
def auth(
    session: CurrentSyncSession,
    authorization: str = Header(),
):
    """Auth function based on header."""
    token = authorization.split(" ")[-1]
    return authenthicate_user(token, session)


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
