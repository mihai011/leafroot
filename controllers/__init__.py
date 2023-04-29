"""Start of the controller module."""

import string
import logging
from typing import Annotated

from fastapi.responses import ORJSONResponse
from fastapi import Header, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from motor.motor_asyncio import AsyncIOMotorClient

from data import User, get_async_session, get_sync_session, get_mongo_database
from utils import authenthicate_user
from logger import log


@log()
def auth(
    authorization: str = Header(), session: Session = Depends(get_sync_session)
):
    """Auth function based on header."""
    token = authorization.split(" ")[-1]
    return authenthicate_user(token, session)


@log()
async def parse(request):
    """Simple parser for request."""
    if request.method == "GET":
        args = request.query_params._dict

    if request.method == "POST":
        args = await request.json()

    return args


@log()
def create_response(message: string, status: int, item=None) -> ORJSONResponse:
    """Receive a message parameter from which a reponse is created and item
    from wich a dictionay is ORJSONResponse object is made as response."""
    data = {}
    data["message"] = message
    data["item"] = item
    data["status"] = status

    logging.info("Creating response with data:%s", str(data))
    return ORJSONResponse(content=data)


CurrentUser = Annotated[User, Depends(auth)]
CurrentSession = Annotated[AsyncSession, Depends(get_async_session)]
MongoDatabase = Annotated[AsyncIOMotorClient, Depends(get_mongo_database)]
