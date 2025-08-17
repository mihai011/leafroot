"""KeyValues packet model."""

from __future__ import annotations

from pydantic import BaseModel


class KeyValuePacket(BaseModel):
    """KeyValue Packet."""

    key: str
    value: int | str
