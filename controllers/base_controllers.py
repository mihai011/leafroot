"""base controller for stage."""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from controllers import auth_decorator
from data import get_session

base_router = APIRouter(prefix="", tags=["base"])
templates = Jinja2Templates(directory="templates")


@base_router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    """Simple login page"""

    return templates.TemplateResponse("login.html", {"request": request})


@base_router.get("/main", response_class=HTMLResponse)
@auth_decorator
async def main(request: Request):
    """Simple main page"""

    return templates.TemplateResponse("main.html", {"request": request})
