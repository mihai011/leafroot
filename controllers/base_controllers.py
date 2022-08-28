"""base controller for stage."""

from fastapi import APIRouter

from controllers import create_response

base_router = APIRouter(prefix="", tags=["base"])


@base_router.get(
    "/",
)
async def greeting():
    """just a simple greeting."""

    return create_response("Hello World", 200)
