"""Api controllers."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import CurrentUser, HttpSession, create_response
from data import BaseResponse, HttpRequest
from logger import log
from utils.external_api import make_api_request

api_router = APIRouter(prefix="/api", tags=["api"])


@log()
@api_router.post("/external", response_model=BaseResponse)
async def api_request(
    http_request: HttpRequest,
    _: CurrentUser,
    http_session: HttpSession,
) -> ORJSONResponse:
    """Make a http request to an external api."""
    response = await make_api_request(http_session, http_request)

    return create_response(
        message="Api called",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=response,
    )
