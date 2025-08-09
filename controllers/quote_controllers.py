"""Quote controller."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import (
    CurrentAsyncSession,
    CurrentUser,
    create_response,
)
from data import PydanticQuote, QuoteResponseItem
from data.models.postgresql.quote import Quote
from services.quote_service import get_random_quote

quotes_router = APIRouter(prefix="/quotes", tags=["quote"])


@quotes_router.get("/quote", response_model=QuoteResponseItem)
async def get_quote(_: CurrentUser, session: CurrentAsyncSession) -> ORJSONResponse:
    """Returns a random quote from the database."""

    quote = await get_random_quote(session)

    return create_response(
        message="Quote retrieved!",
        status=status.HTTP_200_OK,
        response_model=QuoteResponseItem,
        item=quote.serialize(),
    )


@quotes_router.post("/quote", response_model=QuoteResponseItem)
async def create_quote(
    quote: PydanticQuote,
    _: CurrentUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """Creates a quote object."""

    quote = await Quote.AddNew(session, quote.dict())

    return create_response(
        message="Quote created succesfully!",
        status=status.HTTP_200_OK,
        response_model=QuoteResponseItem,
        item=quote.serialize(),
    )
