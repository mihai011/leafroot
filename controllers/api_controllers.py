"""Api controllers."""
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser
from data import HttpRequest
from utils.external_api import get_http_session, make_api_request
from logger import log

api_router = APIRouter(prefix="/api", tags=["api"])


@log()
@api_router.post("/external")
async def api_request(
    http_request: HttpRequest,
    payload: CurrentUser,
    http_session=Depends(get_http_session),
) -> ORJSONResponse:
    """Make a http request to an external api."""

    response = await make_api_request(http_session, http_request)

    return create_response("api called", 200, response)
