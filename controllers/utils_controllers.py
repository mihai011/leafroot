"""Health controller."""
import logging

from fastapi import Request, APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from data import get_session
from external_api.utils import get_http_session, make_api_request
from controllers import create_response, auth_decorator, parse
from services.health_service import health_check

utils_router = APIRouter(prefix="/utils", tags=["utils"])


@utils_router.get("/health_check")
@auth_decorator
async def get_health_check(
    request: Request, session: AsyncSession = Depends(get_session)
):

    status = await health_check()

    return create_response("Status retrieved!", 200, status)
