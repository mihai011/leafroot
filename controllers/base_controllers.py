from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import get_session
from controllers import create_response_ok,\
    create_bulk_users, create_response_bad

from data import User, Token

base_router = APIRouter(prefix="",
                        tags=["base"])


@base_router.get("/", )
async def greeting():

    return create_response_ok("Hello World")
