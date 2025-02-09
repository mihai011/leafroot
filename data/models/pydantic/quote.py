"""Pydantic quotes classes."""

from pydantic import BaseModel


class PydanticQuote(BaseModel):
    """Pydantic class Quote."""

    quote: str
    author: str
