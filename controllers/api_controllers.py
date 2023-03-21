"""Api controllers."""
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser
from data import HttpRequest
from external_api.utils import get_http_session, make_api_request
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
    # if "url" not in content:
    #     return create_response("Url not found in payload!", 400)
    # if "method" not in content:
    #     return create_response("Method not found in payload!", 400)
    # if "body" not in content:
    #     return create_response("Body not found in payload!", 400)
    # if "params" not in content:
    #     return create_response("Params not found in payload!", 400)
    # if "headers" not in content:
    #     return create_response("Headers not found in payload!", 400)

    response = await make_api_request(http_session, http_request)

    return create_response("api called", 200, response)
