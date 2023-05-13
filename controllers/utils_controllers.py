"""Health controller."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from data import StatusResponseItem
from controllers import create_response, CurrentUser
from services.health_service import health_check

utils_router = APIRouter(prefix="/utils", tags=["utils"])


@utils_router.get("/health_check", response_model=StatusResponseItem)
async def get_health_check(_: CurrentUser) -> ORJSONResponse:
    """Returns the health state of the system."""

    health_status = await health_check()

    return create_response(
        message="Status retrieved!",
        status=status.HTTP_200_OK,
        response_model=StatusResponseItem,
        item=health_status,
    )
