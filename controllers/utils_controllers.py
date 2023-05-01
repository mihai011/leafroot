"""Health controller."""

from fastapi import Request, APIRouter
from fastapi.responses import ORJSONResponse

from data.models.postgresql.quote import Quote
from controllers import (
    create_response,
    parse,
    CurrentUser,
    CurrentAsyncSession,
)
from services.health_service import health_check
from services.quote_service import get_random_quote

utils_router = APIRouter(prefix="/utils", tags=["utils"])


@utils_router.get("/health_check")
async def get_health_check(
    _: CurrentUser,
):
    """Returns the health state of the system."""

    status = await health_check()

    return create_response("Status retrieved!", 200, status)


@utils_router.get("/quote")
async def get_quote(_: CurrentUser, session: CurrentAsyncSession):
    """Returns a random quote from the database."""

    quote = await get_random_quote(session)

    return create_response("Quote retrieved!", 200, quote.serialize())


@utils_router.post("/quote")
async def create_quote(
    request: Request,
    _: CurrentUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """Creates a quote object."""

    params = await parse(request)
    quote = await Quote.AddNew(session, params)

    await session.close()
    return create_response(
        "Quote created succesfully!", 200, quote.serialize()
    )
