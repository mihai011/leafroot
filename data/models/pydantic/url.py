"""Url packets"""

from pydantic import BaseModel, HttpUrl


class UrlPacket(BaseModel):
    """Basic URLPacket"""

    url: HttpUrl
