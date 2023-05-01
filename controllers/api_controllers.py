"""Api controllers."""
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser, HttpSession
from data import HttpRequest
from utils.external_api import make_api_request
from logger import log

api_router = APIRouter(prefix="/api", tags=["api"])


@log()
@api_router.post("/external")
async def api_request(
    http_request: HttpRequest,
    _: CurrentUser,
    http_session: HttpSession,
) -> ORJSONResponse:
    """Make a http request to an external api."""

    response = await make_api_request(http_session, http_request)

    return create_response("api called", 200, response)
