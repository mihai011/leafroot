"""base controller for stage."""

import requests
import aiohttp

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from controllers import auth

base_router = APIRouter(prefix="", tags=["base"])
templates = Jinja2Templates(directory="templates")


@base_router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    """Simple login page."""

    return templates.TemplateResponse("login.html", {"request": request})


@base_router.get("/main", response_class=HTMLResponse)
async def main(request: Request, payload: dict = Depends(auth)):
    """Simple main page."""

    return templates.TemplateResponse("main.html", {"request": request})


@base_router.get("/sync_controller", response_class=JSONResponse)
def sync(request: Request):
    """Simple sync controller."""

    requests.get("http://google.com", timeout=1)

    return {"status": 200}


@base_router.get("/async_controller", response_class=JSONResponse)
async def async_func(request: Request):
    """Simple async controller."""
    async with aiohttp.ClientSession() as session:
        await session.get("http://google.com", timeout=1)

    return {"status": 200}
