"""Module for quotes functions."""

from sqlalchemy.orm import Session

from data import Quote


async def get_random_quote(session: Session) -> Quote:
    """Retreives a random Quote."""
    return await Quote.get_random(session)
