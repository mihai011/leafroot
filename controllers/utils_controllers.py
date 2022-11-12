"""Health controller."""
import logging

from fastapi import Request, APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from data import get_session
from data.models.quote import Quote
from controllers import create_response, auth_decorator, parse
from services.health_service import health_check
from services.quote_service import get_random_quote

utils_router = APIRouter(prefix="/utils", tags=["utils"])


@utils_router.get("/health_check")
@auth_decorator
async def get_health_check(
    request: Request, session: AsyncSession = Depends(get_session)
):
    """Returns the health state of the system."""

    status = await health_check()

    return create_response("Status retrieved!", 200, status)


@utils_router.get("/quote")
@auth_decorator
async def get_quote(
    request: Request, session: AsyncSession = Depends(get_session)
):
    """Returns a random quote from the database."""

    quote = await get_random_quote(session)

    return create_response("Quote retrieved!", 200, quote.serialize())


@utils_router.post("/quote")
@auth_decorator
async def create_quote(
    request: Request, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    """Creates a quote object."""

    params = await parse(request)
    quote = await Quote.AddNew(session, params)

    await session.close()
    return create_response(
        "Quote created succesfully!", 200, quote.serialize()
    )
