"""base controller for stage."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

base_router = APIRouter(prefix="", tags=["base"])
templates = Jinja2Templates(directory="templates")


@base_router.get("/", response_class=HTMLResponse)
async def greeting(request: Request):
    """Simple html page"""

    return templates.TemplateResponse(
        "main.html", {"request": request, "id": 1000}
    )
