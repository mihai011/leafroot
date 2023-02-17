"""base controller for stage."""

import requests
import aiohttp

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from controllers import auth_decorator
from data import get_session, get_redis_connection

base_router = APIRouter(prefix="", tags=["base"])
templates = Jinja2Templates(directory="templates")


@base_router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    """Simple login page."""

    return templates.TemplateResponse("login.html", {"request": request})


@base_router.get("/main", response_class=HTMLResponse)
@auth_decorator
async def main(
    request: Request,
    session: AsyncSession = Depends(get_session),  # pylint: disable=W0613
    redis_connection: Redis = Depends(get_redis_connection),
):
    """Simple main page."""

    return templates.TemplateResponse("main.html", {"request": request})


@base_router.get("/sync_controller", response_class=JSONResponse)
def sync(request: Request):
    """! Simple sync controller.

    @param request (Request): Request object
    """

    requests.get("http://google.com")

    return {"status": 200}


@base_router.get("/async_controller", response_class=JSONResponse)
async def control(request: Request):
    """! Simple async controller.

    @param request (Request): Request object
    """
    async with aiohttp.ClientSession() as session:
        await session.get("http://google.com")

    return {"status": 200}
